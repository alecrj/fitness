"""Utilities for database migrations in Firestore"""
import firebase_admin
from firebase_admin import firestore
import time
import logging
import argparse
import importlib
import os
import sys
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('migrations')

# Migration registry
MIGRATIONS = {}

def migration(version):
    """Decorator to register a migration function
    
    Args:
        version: Migration version (e.g., '001', '002')
        
    Returns:
        Decorated function
    """
    def decorator(f):
        MIGRATIONS[version] = f
        return f
    return decorator

def run_migration(version, dry_run=False):
    """Run a specific migration
    
    Args:
        version: Migration version to run
        dry_run: Whether to perform a dry run (no changes)
        
    Returns:
        Success status (bool)
    """
    if version not in MIGRATIONS:
        logger.error(f"Migration {version} not found")
        return False
        
    migration_func = MIGRATIONS[version]
    
    try:
        # Start transaction if not dry run
        db = firebase_admin.firestore.client()
        
        # Get or create migrations collection
        migrations_ref = db.collection('_migrations')
        
        # Check if already applied
        migration_doc = migrations_ref.document(version).get()
        if migration_doc.exists:
            logger.info(f"Migration {version} already applied")
            return True
            
        logger.info(f"Running migration {version}: {migration_func.__name__}")
        
        # Run the migration
        if dry_run:
            logger.info("DRY RUN - No changes will be made")
            migration_func(db, dry_run=True)
        else:
            # Record migration start
            start_time = time.time()
            migrations_ref.document(version).set({
                'version': version,
                'name': migration_func.__name__,
                'started_at': firestore.SERVER_TIMESTAMP,
                'status': 'in_progress'
            })
            
            # Run migration
            migration_func(db, dry_run=False)
            
            # Record migration completion
            end_time = time.time()
            duration = end_time - start_time
            migrations_ref.document(version).update({
                'completed_at': firestore.SERVER_TIMESTAMP,
                'duration_seconds': duration,
                'status': 'completed'
            })
            
        logger.info(f"Migration {version} completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Migration {version} failed: {str(e)}", exc_info=True)
        
        # Record failure if not dry run
        if not dry_run:
            migrations_ref.document(version).update({
                'status': 'failed',
                'error': str(e)
            })
            
        return False

def get_pending_migrations():
    """Get list of migrations that haven't been applied yet
    
    Returns:
        List of pending migration versions, sorted
    """
    db = firebase_admin.firestore.client()
    migrations_ref = db.collection('_migrations')
    
    # Get all applied migrations
    applied = {}
    for doc in migrations_ref.stream():
        migration_data = doc.to_dict()
        if migration_data.get('status') == 'completed':
            applied[doc.id] = migration_data
            
    # Find pending migrations
    pending = []
    for version in sorted(MIGRATIONS.keys()):
        if version not in applied:
            pending.append(version)
            
    return pending

def load_migrations_from_directory(directory):
    """Load migration modules from a directory
    
    Args:
        directory: Directory path containing migration files
    """
    sys.path.insert(0, os.path.abspath(directory))
    
    for filename in sorted(os.listdir(directory)):
        if filename.endswith('.py') and filename.startswith('migrate_'):
            module_name = filename[:-3]  # Remove .py extension
            importlib.import_module(module_name)
            
    logger.info(f"Loaded {len(MIGRATIONS)} migrations")

def main():
    """Main entry point for the migration tool"""
    parser = argparse.ArgumentParser(description='Firestore database migration tool')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without making changes')
    parser.add_argument('--list', action='store_true', help='List all migrations and their status')
    parser.add_argument('--run', help='Run a specific migration by version')
    parser.add_argument('--run-pending', action='store_true', help='Run all pending migrations')
    parser.add_argument('--dir', default='./migrations', help='Directory containing migration files')
    
    args = parser.parse_args()
    
    # Initialize Firebase (assuming credentials are set in environment)
    try:
        firebase_admin.get_app()
    except ValueError:
        # App not initialized
        from config import Config
        firebase_admin.initialize_app(
            firebase_admin.credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
        )
    
    # Load migrations
    load_migrations_from_directory(args.dir)
    
    if args.list:
        # List migrations and their status
        db = firebase_admin.firestore.client()
        migrations_ref = db.collection('_migrations')
        
        # Get all applied migrations
        applied = {}
        for doc in migrations_ref.stream():
            applied[doc.id] = doc.to_dict()
            
        # Display migrations
        print("\nMigration Status:")
        print("-----------------")
        
        for version in sorted(MIGRATIONS.keys()):
            migration_func = MIGRATIONS[version]
            status = "PENDING"
            
            if version in applied:
                migration_data = applied[version]
                status = migration_data.get('status', 'unknown').upper()
                
                # Add completion time if available
                if 'completed_at' in migration_data:
                    completed_at = migration_data['completed_at']
                    if isinstance(completed_at, datetime):
                        status += f" ({completed_at.strftime('%Y-%m-%d %H:%M:%S')})"
                    
            print(f"{version}: {migration_func.__name__} - {status}")
            
        print()
        
    elif args.run:
        # Run a specific migration
        success = run_migration(args.run, dry_run=args.dry_run)
        if not success:
            sys.exit(1)
            
    elif args.run_pending:
        # Run all pending migrations
        pending = get_pending_migrations()
        
        if not pending:
            logger.info("No pending migrations")
            return
            
        logger.info(f"Running {len(pending)} pending migrations")
        
        for version in pending:
            success = run_migration(version, dry_run=args.dry_run)
            if not success:
                logger.error(f"Stopping after failed migration {version}")
                sys.exit(1)
                
        logger.info("All pending migrations completed successfully")
        
    else:
        parser.print_help()

if __name__ == '__main__':
    main()