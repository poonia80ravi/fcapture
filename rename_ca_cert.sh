#!/bin/bash

# Check if the certificate file path is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <path_to_certificate_file>"
  exit 1
fi

# Get the certificate file path from the first argument
cert_file_path="$1"

# Get the directory and filename from the certificate file path
cert_folder=$(dirname "$cert_file_path")
cert_file=$(basename "$cert_file_path")

# Change to the specified certificate folder
cd "$cert_folder" || { echo "Failed to change directory to $cert_folder"; exit 1; }

# Generate the hash for the certificate
hashed_name=$(openssl x509 -inform PEM -subject_hash_old -in "$cert_file" | head -1)

# Check if the hash generation was successful
if [ -z "$hashed_name" ]; then
  echo "Failed to generate hash for the certificate."
  exit 1
fi

# Copy the certificate to the new file with the hashed name
cp "$cert_file" "$hashed_name.0"

# Confirm the operation
if [ $? -eq 0 ]; then
  echo "Certificate copied to $hashed_name.0 successfully."
else
  echo "Failed to copy the certificate."
  exit 1
fi

