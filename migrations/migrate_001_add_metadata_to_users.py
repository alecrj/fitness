"""Migration to add metadata fields to users collection"""
import logging
from utils.migrations import migration

logger = logging.getLogger('migrations')

@migration('001')
def add_metadata_to_users(db, dry_run=False):
    """Add metadata fields to users collection
    
    Args:
        db: Firestore client
        dry_run: Whether to perform a dry run (no changes)
    """
    # Get users collection
    users_ref = db.collection('users')
    batch_size = 500
    batches_processed = 0
    docs_updated = 0
    
    # Process in batches to avoid memory issues with large collections
    query = users_ref.limit(batch_size)
    docs = query.stream()
    all_docs = list(docs)
    
    while all_docs:
        batch = db.batch()
        batch_updates = 0
        
        for doc in all_docs:
            user_data = doc.to_dict()
            updates = {}
            
            # Add last_active_at if missing
            if 'last_active_at' not in user_data:
                updates['last_active_at'] = user_data.get('updated_at') or user_data.get('created_at')
                
            # Add version field if missing
            if 'version' not in user_data:
                updates['version'] = 1
                
            # Add metadata field if missing
            if 'metadata' not in user_data:
                updates['metadata'] = {
                    'onboarding_completed': 'profile_image_url' in user_data,
                    'migration': 'v1'
                }
                
            # Skip if no updates needed
            if not updates:
                continue
                
            # Apply updates
            if not dry_run:
                batch.update(doc.reference, updates)
                batch_updates += 1
            
            docs_updated += 1
            
        # Commit batch if not dry run and has updates
        if not dry_run and batch_updates > 0:
            batch.commit()
            
        batches_processed += 1
        logger.info(f"Processed batch {batches_processed} ({len(all_docs)} docs)")
        
        # Get next batch
        last_doc = all_docs[-1]
        query = users_ref.limit(batch_size).start_after(last_doc)
        all_docs = list(query.stream())
        
    # Log summary
    logger.info(f"Migration complete: processed {batches_processed} batches, updated {docs_updated} documents")