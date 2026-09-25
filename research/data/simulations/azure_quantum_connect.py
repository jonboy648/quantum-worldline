"""
Test Azure Quantum workspace connection using azure-quantum SDK.
Uses connection string with API key (from portal Access Keys page).
Set AZURE_QUANTUM_CONNECTION_STRING env var or pass directly.
"""
import os
from azure.quantum import Workspace

# Connection string from Azure Portal > Access Keys
# Format: SubscriptionId=...;ResourceGroupName=...;WorkspaceName=...;ApiKey=...;QuantumEndpoint=...
CONNECTION_STRING = os.environ.get("AZURE_QUANTUM_CONNECTION_STRING", "")

if not CONNECTION_STRING:
    print("ERROR: Set AZURE_QUANTUM_CONNECTION_STRING environment variable")
    print("Get it from: Azure Portal > quantum-worldline > Operations > Access Keys")
    exit(1)

print("Connecting via API key...")
workspace = Workspace.from_connection_string(CONNECTION_STRING)

print(f"Connected to workspace: {workspace.name}")
print(f"Location: {workspace.location}")

# List available targets
print("\nAvailable targets:")
for target in workspace.get_targets():
    print(f"  {target.name} ({target.provider_id}) - {target.current_availability}")

print("\nWorkspace connection: SUCCESS")
