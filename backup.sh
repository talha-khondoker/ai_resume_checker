#!/bin/bash

# Backup and restore utilities for production

case "$1" in
  backup)
    echo "Creating database backup..."
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U $DB_USER $DB_NAME > backups/backup_${TIMESTAMP}.sql
    echo "✅ Backup created: backups/backup_${TIMESTAMP}.sql"
    echo "Compressing backup..."
    gzip backups/backup_${TIMESTAMP}.sql
    echo "✅ Compressed: backups/backup_${TIMESTAMP}.sql.gz"
    ;;
    
  restore)
    if [ -z "$2" ]; then
      echo "❌ Please provide backup file"
      echo "Usage: ./backup.sh restore backups/backup_20240101_120000.sql"
      exit 1
    fi
    echo "Restoring database from $2..."
    docker-compose -f docker-compose.prod.yml exec -T postgres psql -U $DB_USER $DB_NAME < $2
    echo "✅ Restore complete!"
    ;;
    
  list)
    echo "Available backups:"
    ls -lh backups/
    ;;
    
  clean)
    echo "Removing old backups (older than 30 days)..."
    find backups -name "backup_*.sql.gz" -mtime +30 -delete
    echo "✅ Old backups cleaned"
    ;;
    
  *)
    echo "Database backup utility"
    echo ""
    echo "Usage:"
    echo "  ./backup.sh backup          - Create backup"
    echo "  ./backup.sh restore <file>  - Restore from backup"
    echo "  ./backup.sh list            - List backups"
    echo "  ./backup.sh clean           - Remove old backups"
    ;;
esac
