#!/usr/bin/env python3

"""
Deployment Configuration Generator
Generates environment variables and configuration files for different platforms
"""

import os
import secrets
import argparse
import json
from pathlib import Path


def generate_secret_key():
    """Generate a secure secret key for JWT"""
    return secrets.token_urlsafe(32)


def generate_db_password():
    """Generate a strong database password"""
    return secrets.token_urlsafe(32)


def create_env_file(platform, domain, output_path):
    """Create environment file for specified platform"""
    
    secret_key = generate_secret_key()
    db_password = generate_db_password()
    
    if platform == "heroku":
        env_content = f"""# Heroku Deployment
FLASK_ENV=production
DEBUG=False
SECRET_KEY={secret_key}
ALGORITHM=HS256
ALLOWED_ORIGINS=https://<YOUR_APP_NAME>.herokuapp.com
NEXT_PUBLIC_API_URL=https://<YOUR_APP_NAME>.herokuapp.com
"""
    elif platform == "aws":
        env_content = f"""# AWS Deployment
DEBUG=False
SECRET_KEY={secret_key}
DB_PASSWORD={db_password}
ALLOWED_ORIGINS=https://{domain}
NEXT_PUBLIC_API_URL=https://{domain}
"""
    elif platform == "digitalocean":
        env_content = f"""# DigitalOcean Deployment
DEBUG=False
SECRET_KEY={secret_key}
DB_PASSWORD={db_password}
ALLOWED_ORIGINS=https://{domain},https://www.{domain}
NEXT_PUBLIC_API_URL=https://{domain}
"""
    elif platform == "gcp":
        env_content = f"""# Google Cloud Deployment
DEBUG=False
SECRET_KEY={secret_key}
DB_PASSWORD={db_password}
ALLOWED_ORIGINS=https://{domain}
NEXT_PUBLIC_API_URL=https://{domain}
"""
    else:
        env_content = f"""# Generic Cloud Deployment
DEBUG=False
SECRET_KEY={secret_key}
DB_PASSWORD={db_password}
ALLOWED_ORIGINS=https://{domain}
NEXT_PUBLIC_API_URL=https://{domain}
"""
    
    with open(output_path, 'w') as f:
        f.write(env_content)
    
    print(f"✅ Environment file created: {output_path}")
    return env_content


def create_deployment_config(platform):
    """Create deployment configuration for specified platform"""
    
    configs = {
        "heroku": {
            "dynos": "web:1 worker:1",
            "addons": ["heroku-postgresql", "sendgrid"],
            "regions": ["us", "eu"],
        },
        "aws": {
            "instance_type": "t3.medium",
            "rds_class": "db.t3.micro",
            "elb_type": "application",
        },
        "digitalocean": {
            "droplet_size": "$12/month",
            "database_size": "$12/month",
            "region": "nyc3",
        },
        "gcp": {
            "compute_machine": "e2-medium",
            "cloud_sql_tier": "db-f1-micro",
            "region": "us-central1",
        }
    }
    
    return configs.get(platform, {})


def main():
    parser = argparse.ArgumentParser(description="Generate deployment configurations")
    parser.add_argument(
        "--platform",
        choices=["heroku", "aws", "digitalocean", "gcp", "all"],
        default="all",
        help="Target deployment platform"
    )
    parser.add_argument(
        "--domain",
        type=str,
        default="yourdomain.com",
        help="Domain name for the application"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=".",
        help="Output directory"
    )
    
    args = parser.parse_args()
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    platforms = ["heroku", "aws", "digitalocean", "gcp"] if args.platform == "all" else [args.platform]
    
    for platform in platforms:
        print(f"\n{'='*50}")
        print(f"Generating configuration for: {platform.upper()}")
        print(f"{'='*50}")
        
        # Create env file
        env_file = output_dir / f".env.{platform}"
        create_env_file(platform, args.domain, env_file)
        
        # Create config file
        config = create_deployment_config(platform)
        config_file = output_dir / f"config.{platform}.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"✅ Configuration file created: {config_file}")
    
    print(f"\n{'='*50}")
    print("✅ All configurations generated successfully!")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
