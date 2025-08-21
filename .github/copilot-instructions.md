# Fiscalberry Copilot Instructions

## Architecture Overview

Fiscalberry is a multi-platform fiscal printer server that bridges JSON commands to physical printer hardware. It operates in three modes:
- **CLI mode** (`fiscalberry_cli`) - Headless service for production/Raspberry Pi
- **GUI mode** (`fiscalberry_gui`) - Kivy-based desktop interface
- **Android** - Mobile app built with Buildozer

### Core Components

- `ServiceController` - Singleton managing SocketIO connections and service lifecycle
- `FiscalberrySio` - WebSocket handler for client communication
- `ComandosHandler` - JSON command translation to printer-specific protocols
- `Configberry` - Configuration management with priority: config.ini > SocketIO messages
- `RabbitMQProcessHandler` - Message queue integration for enterprise deployments

### Data Flow
1. Client sends JSON via WebSocket → `FiscalberrySio`
2. Commands routed to `ComandosHandler` → printer drivers (`EscPComandos`, `FiscalberryComandos`)
3. Responses flow back through same chain to client

## Development Workflows

### Environment Setup
```bash
# Create separate environments for different modes
python3 -m venv venv.cli && source venv.cli/bin/activate
pip install -r requirements.cli.txt

python3 -m venv venv.kivy && source venv.kivy/bin/activate  
pip install -r requirements.kivy.txt
```

### Running Services
```bash
# CLI mode (production)
python src/fiscalberry/cli.py

# GUI mode (development)
python src/fiscalberry/gui.py

# Direct service controller
python src/main.py
```

### Building
```bash
# PyInstaller specs for executables
pyinstaller fiscalberry-cli.spec  # Linux/Windows CLI
pyinstaller fiscalberry-gui.spec  # GUI version

# Android build
buildozer android debug
```

## Project-Specific Patterns

### Configuration Priority
Config values follow strict precedence: `config.ini` settings override SocketIO message parameters. Use `get_config_or_message_value()` pattern in RabbitMQ setup.

### Error Handling
- **DNS errors**: Use exponential backoff in `RabbitMQProcessHandler`
- **Connection failures**: Implement graceful degradation with descriptive user messages
- **Printer errors**: Queue commands with `print_queue` (max 100 items)

### Threading Model
- `ServiceController` manages persistent SocketIO connections with auto-reconnect
- Use `_stop_event` threading.Event for graceful shutdown
- Background processes marked with `daemon=True` for CLI mode

### Driver Architecture
Commands are abstracted through:
1. JSON → `ComandosHandler.procesar()` 
2. Driver selection based on printer type (Fiscal/Receipt)
3. Protocol translation (`EscPComandos` for receipt, `FiscalberryComandos` for fiscal)

## Integration Points

### RabbitMQ Integration
- Optional enterprise feature for message queuing
- Uses `pika` with connection pooling
- Diagnostic tools in `src/fiscalberry/diagnostics/rabbitmq_check.py`

### Cross-Platform Considerations
- Windows: Include `pywin32` dependency
- Android: Remove desktop-only deps from `buildozer.spec`
- Linux service: Use `fiscalberry.service` systemd unit

### Key File Patterns
- Entry points: `src/fiscalberry/{cli,gui}.py`
- Config location: `platformdirs.user_config_dir('Fiscalberry')/config.ini`
- Logging: Centralized through `fiscalberry_logger.getLogger()`
- Assets: `src/fiscalberry/ui/assets/` for GUI resources

## Testing & Diagnostics

Run integration tests with:
```bash
python test_config_priority.py  # Config precedence logic
python src/fiscalberry/diagnostics/rabbitmq_check.py  # Network connectivity
```

### Common Debug Commands
- Check printer detection: Monitor `printer_detector.py` logs
- RabbitMQ issues: Use diagnostic script with `--host`, `--user` flags
- Service status: Query `ServiceController.is_service_running()`
