# PyQt5 Battery Widget

A customizable battery widget implementation using PyQt5, perfect for visualizing battery levels, 
voltage readings, or any other percentage-based indicators in your Qt applications.

![image](https://github.com/user-attachments/assets/6ba32cc9-5337-4b17-a41e-442a35441ab5)

## Features

- Customizable battery visualization with segmented fill
- Support for both horizontal and vertical orientations
- Configurable number of segments
- Adjustable minimum and maximum voltage ranges
- Smooth updates with real-time voltage changes
- Anti-aliased rendering for crisp appearance
- Customizable colors for filled and empty segments

## Requirements

- Python 3.6+
- PyQt5

## Installation

1. Install the required dependencies:
```bash
pip install PyQt5
```

2. Clone this repository:
```bash
git clone https://github.com/yourusername/pyqt5-battery-widget.git
cd pyqt5-battery-widget
```

## Usage

### Basic Usage

```python
from PyQt5.QtWidgets import QApplication
from battery_widget import BatteryWidget

app = QApplication([])
battery = BatteryWidget(
    min_voltage=0.0,
    max_voltage=5.0,
    segments=10
)
battery.show()
app.exec_()
```

### Customization Examples

1. Create a horizontal battery widget:
```python
battery = BatteryWidget(
    orientation=Qt.Horizontal,
    segments=10,
    min_voltage=0.0,
    max_voltage=5.0
)
```

2. Create a vertical battery widget:
```python
battery = BatteryWidget(
    orientation=Qt.Vertical,
    segments=8,
    min_voltage=0.0,
    max_voltage=12.0
)
```

3. Update voltage programmatically:
```python
battery.voltage = 3.7  # Sets voltage to 3.7V
```

## API Reference

### BatteryWidget

#### Constructor Parameters

- `parent` (QWidget, optional): Parent widget. Defaults to None.
- `min_voltage` (float, optional): Minimum voltage value. Defaults to 0.0.
- `max_voltage` (float, optional): Maximum voltage value. Defaults to 100.0.
- `segments` (int, optional): Number of fill segments. Defaults to 10.
- `orientation` (Qt.Orientation, optional): Widget orientation. Defaults to Qt.Horizontal.

#### Properties

- `voltage` (float): Get/set current voltage value
- `min_voltage` (float): Get/set minimum voltage value
- `max_voltage` (float): Get/set maximum voltage value
- `segments` (int): Get/set number of segments
- `orientation` (Qt.Orientation): Get/set widget orientation

### BatteryWidgetDemo

A demonstration application showcasing the BatteryWidget capabilities.

## Example

```python
import sys
from PyQt5.QtWidgets import QApplication
from battery_widget import BatteryWidgetDemo

def main():
    app = QApplication(sys.argv)
    demo = BatteryWidgetDemo()
    demo.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

## Widget Appearance

The battery widget features:
- A main body rectangle with segmented fill
- A terminal tip
- Configurable number of segments
- Green color for filled segments
- Light gray color for empty segments
- Black outline for clear visibility

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the need for a customizable battery widget in Qt applications
- Thanks to the PyQt community for the excellent framework

## Author

Yamil Garcia

## Version History

- 1.0.0
    - Initial release
    - Basic battery widget implementation
    - Horizontal and vertical orientations
    - Demo application

