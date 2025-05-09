#!/usr/bin/env python3
"""Management script for common maintenance tasks"""
import os
import sys
import argparse
import subprocess
import logging
import firebase_admin
from firebase_admin import credentials
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('manage')

def init_firebase():
    """Initialize Firebase connection"""
    try:
        firebase_admin.get_app()
    except ValueError:
        # Initialize Firebase
        cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS_PATH)
        firebase_admin.initialize_app(cred, {
            'storageBucket': Config.FIREBASE_STORAGE_BUCKET
        })
    return firebase_admin.firestore.client()

def run_tests(args):
    """Run application tests"""
    test_path = args.path or 'tests'
    verbose = '-v' if args.verbose else ''
    
    cmd = f"python -m unittest discover {test_path} {verbose}"
    logger.info(f"Running tests: {cmd}")
    
    # Run tests
    result = subprocess.run(cmd, shell=True)
    return result.returncode

def run_migrations(args):
    """Run database migrations"""
    from utils.migrations import main as migrations_main
    
    # Update sys.argv for migrations
    sys.argv = ['manage.py']
    
    if args.list:
        sys.argv.append('--list')
    elif args.run:
        sys.argv.extend(['--run', args.run])
    elif args.dry_run:
        sys.argv.append('--dry-run')
        sys.argv.append('--run-pending')
    else:
        sys.argv.append('--run-pending')
        
    # Run migrations
    migrations_main()
    return 0

def create_migration(args):
    """Create a new migration file"""
    migration_id = args.id
    migration_name = args.name.lower().replace(' ', '_')
    
    # Ensure migrations directory exists
    os.makedirs('migrations', exist_ok=True)
    
    # Create migration filename
    filename = f"migrations/migrate_{migration_id}_{migration_name}.py"
    
    # Check if file already exists
    if os.path.exists(filename):
        logger.error(f"Migration file already exists: {filename}")
        return 1
        
    # Create migration file
    with open(filename, 'w') as f:
        f.write(f'''"""Migration to {args.name}"""
import logging
from utils.migrations import migration

logger = logging.getLogger('migrations')

@migration('{migration_id}')
def {migration_name}(db, dry_run=False):
    """Migration to {args.name}
    
    Args:
        db: Firestore client
        dry_run: Whether to perform a dry run (no changes)
    """
    # TODO: Implement migration
    logger.info("Starting migration")
    
    # Example migration code:
    # collection_ref = db.collection('your_collection')
    # batch_size = 500
    # query = collection_ref.limit(batch_size)
    # docs = list(query.stream())
    
    # while docs:
    #     batch = db.batch()
    #     
    #     for doc in docs:
    #         # Process each document
    #         if not dry_run:
    #             batch.update(doc.reference, {{'your_field': 'new_value'}})
    #     
    #     # Commit batch if not dry run
    #     if not dry_run:
    #         batch.commit()
    #     
    #     # Get next batch
    #     last_doc = docs[-1]
    #     query = collection_ref.limit(batch_size).start_after(last_doc)
    #     docs = list(query.stream())
    
    logger.info("Migration completed")
''')
    
    logger.info(f"Created migration file: {filename}")
    return 0

def run_server(args):
    """Run the development server"""
    from app import create_app
    
    app = create_app()
    host = args.host or Config.HOST
    port = args.port or Config.PORT
    debug = args.debug or Config.DEBUG
    
    logger.info(f"Starting server on {host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)
    return 0

def backup_database(args):
    """Create a backup of Firestore database"""
    # Initialize Firebase
    db = init_firebase()
    
    output_dir = args.output_dir or 'backups'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate timestamp for filename
    import datetime
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{output_dir}/backup_{timestamp}.json"
    
    logger.info(f"Starting database backup to {filename}")
    
    # Get all collections
    collections = db.collections()
    backup_data = {}
    
    # Process each collection
    for collection in collections:
        # Skip internal collections if specified
        if args.skip_internal and collection.id.startswith('_'):
            logger.info(f"Skipping internal collection: {collection.id}")
            continue
            
        logger.info(f"Backing up collection: {collection.id}")
        collection_data = {}
        
        # Get all documents in collection
        docs = collection.stream()
        for doc in docs:
            collection_data[doc.id] = doc.to_dict()
            
        backup_data[collection.id] = collection_data
        
    # Write to file
    import json
    with open(filename, 'w') as f:
        json.dump(backup_data, f, default=str, indent=2)
        
    logger.info(f"Backup completed: {filename}")
    return 0

def restore_database(args):
    """Restore Firestore database from backup"""
    if not args.file:
        logger.error("Backup file is required for restore")
        return 1
        
    if not os.path.exists(args.file):
        logger.error(f"Backup file not found: {args.file}")
        return 1
        
    # Confirm restore
    if not args.force:
        confirm = input("This will overwrite data in Firestore. Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            logger.info("Restore cancelled")
            return 0
            
    # Initialize Firebase
    db = init_firebase()
    
    logger.info(f"Starting database restore from {args.file}")
    
    # Load backup data
    import json
    with open(args.file, 'r') as f:
        backup_data = json.load(f)
        
    # Process each collection
    for collection_id, collection_data in backup_data.items():
        logger.info(f"Restoring collection: {collection_id}")
        
        # Skip if empty
        if not collection_data:
            continue
            
        # Process in batches
        batch_size = 500
        batch_count = 0
        batch = db.batch()
        count = 0
        
        for doc_id, doc_data in collection_data.items():
            # Add to batch
            doc_ref = db.collection(collection_id).document(doc_id)
            batch.set(doc_ref, doc_data)
            count += 1
            
            # Commit when batch size reached
            if count >= batch_size:
                batch.commit()
                batch = db.batch()
                count = 0
                batch_count += 1
                logger.info(f"Committed batch {batch_count} for {collection_id}")
                
        # Commit final batch
        if count > 0:
            batch.commit()
            batch_count += 1
            logger.info(f"Committed final batch {batch_count} for {collection_id}")
            
    logger.info("Restore completed")
    return 0

def cleanup_database(args):
    """Clean up old or unused data in Firestore"""
    # Initialize Firebase
    db = init_firebase()
    
    cleanup_days = args.days or 30
    
    # Confirm cleanup
    if not args.force:
        confirm = input(f"This will delete data older than {cleanup_days} days. Are you sure? (y/N): ")
        if confirm.lower() != 'y':
            logger.info("Cleanup cancelled")
            return 0
            
    # Calculate cutoff date
    import datetime
    cutoff = datetime.datetime.now() - datetime.timedelta(days=cleanup_days)
    
    # Clean up old tasks
    if args.tasks:
        logger.info(f"Cleaning up completed tasks older than {cleanup_days} days")
        
        # Query for old completed tasks
        tasks_ref = db.collection('tasks')
        old_tasks = tasks_ref.where('status', 'in', ['completed', 'failed']) \
                            .where('completed_at', '<', cutoff) \
                            .stream()
                            
        # Delete old tasks
        deleted = 0
        for task in old_tasks:
            task.reference.delete()
            deleted += 1
            
        logger.info(f"Deleted {deleted} old tasks")
        
    # Clean up temporary files
    if args.temp_files:
        logger.info(f"Cleaning up temporary files older than {cleanup_days} days")
        
        # This would require listing files in Firebase Storage
        # which is more complex than a simple Firestore query
        # For now, we'll log a message
        logger.info("Temporary file cleanup not implemented yet")
        
    logger.info("Cleanup completed")
    return 0

def main():
    """Main entry point for management script"""
    parser = argparse.ArgumentParser(description='Management script for the application')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.add_argument('--path', help='Test path (default: tests)')
    test_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Migration commands
    migrate_parser = subparsers.add_parser('migrate', help='Run database migrations')
    migrate_parser.add_argument('--list', action='store_true', help='List migrations')
    migrate_parser.add_argument('--run', help='Run specific migration')
    migrate_parser.add_argument('--dry-run', action='store_true', help='Dry run (no changes)')
    
    # Create migration command
    create_migration_parser = subparsers.add_parser('create-migration', help='Create a new migration')
    create_migration_parser.add_argument('id', help='Migration ID (e.g., 001)')
    create_migration_parser.add_argument('name', help='Migration name (e.g., add_user_roles)')
    
    # Run server command
    server_parser = subparsers.add_parser('runserver', help='Run development server')
    server_parser.add_argument('--host', help='Host to listen on')
    server_parser.add_argument('--port', type=int, help='Port to listen on')
    server_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Backup Firestore database')
    backup_parser.add_argument('--output-dir', help='Output directory for backup')
    backup_parser.add_argument('--skip-internal', action='store_true', help='Skip internal collections')
    
    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore Firestore database from backup')
    restore_parser.add_argument('file', help='Backup file to restore from')
    restore_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old data')
    cleanup_parser.add_argument('--days', type=int, help='Delete data older than N days')
    cleanup_parser.add_argument('--tasks', action='store_true', help='Clean up old tasks')
    cleanup_parser.add_argument('--temp-files', action='store_true', help='Clean up temporary files')
    cleanup_parser.add_argument('--force', action='store_true', help='Skip confirmation')
    
    args = parser.parse_args()
    
    # Run appropriate command
    if args.command == 'test':
        return run_tests(args)
    elif args.command == 'migrate':
        return run_migrations(args)
    elif args.command == 'create-migration':
        return create_migration(args)
    elif args.command == 'runserver':
        return run_server(args)
    elif args.command == 'backup':
        return backup_database(args)
    elif args.command == 'restore':
        return restore_database(args)
    elif args.command == 'cleanup':
        return cleanup_database(args)
    else:
        parser.print_help()
        return 0

if __name__ == '__main__':
    sys.exit(main())