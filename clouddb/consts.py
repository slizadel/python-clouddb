VERSION = ".01"

USER_AGENT = 'python-clouddb/%s' % VERSION

# Default AUTH SERVER
DEFAULT_AUTH_SERVER = "https://identity.api.rackspacecloud.com/v1.1/auth"

# UK AUTH SERVER
UK_AUTH_SERVER = "https://lon.identity.api.rackspacecloud.com/v1.1/auth"

# Default URL for Regions
REGION_URL = "https://%s.databases.api.rackspacecloud.com/v1.0"

# Different available Regions
REGION = {
    "chicago": "ord",
    "dallas": "dfw",
    "london": "lon",
}

# Attributed allowed to be modified on databases
# LB_ATTRIBUTES_MODIFIABLE = ["name", "algorithm", "protocol", "port"]

# Types of VirtualIPS
# VIRTUALIP_TYPES = ["PUBLIC", "SERVICENET"]

# HealthMonitors Types
# HEALTH_MONITOR_TYPES = ['CONNECT', 'HTTP', 'HTTPS']

# SessionPersistence Types
# SESSION_PERSISTENCE_TYPES = ['HTTP_COOKIE']
