#!/bin/bash
set -euo pipefail  # Exit on error, undefined vars, and pipeline failures
IFS=$'\n\t'       # Stricter word splitting

# Simple script to allow full internet access
# No firewall restrictions - container has same network access as host

echo "Configuring network for full internet access..."

# Set default policies to ACCEPT (allow all traffic)
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

# Flush any existing rules to ensure clean state
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Clean up any existing ipsets
ipset destroy allowed-domains 2>/dev/null || true

echo "Network configuration complete - full internet access enabled"

# Test connectivity
echo "Testing internet connectivity..."
if curl --connect-timeout 5 https://example.com >/dev/null 2>&1; then
    echo "✓ Internet access verified - able to reach external sites"
else
    echo "⚠ Warning: Could not reach example.com (may be a DNS or network issue)"
fi