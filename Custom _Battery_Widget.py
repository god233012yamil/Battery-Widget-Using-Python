import sys
from math import floor
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QSlider,
    QLabel,
    QHBoxLayout,
)
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QRect, QSize


class BatteryWidget(QWidget):
    """A custom QWidget that displays a battery being charged with segmented fill.

    The battery fills up with green segments as the voltage increases.
    Supports both horizontal and vertical orientations.
    """

    def __init__(
        self,
        parent: QWidget = None,
        min_voltage: float = 0.0, 
        max_voltage: float = 100.0, 
        segments: int = 10,
        orientation: Qt.Orientation = Qt.Horizontal,
    ) -> None:
        """Initialize the BatteryWidget.

        Args:
            parent (QWidget, optional): The parent widget. Defaults to None.
            segments (int, optional): Number of fill segments in the battery. 
            Defaults to 10.
            orientation (Qt.Orientation, optional): Orientation of the battery. 
            Defaults to Qt.Horizontal.
        """
        super().__init__(parent)
        self._voltage: float = 0.0  # Current voltage
        self._min_voltage: float = min_voltage  # Minimum voltage
        self._max_voltage: float = max_voltage  # Maximum voltage
        self._segments: int = segments  # Number of fill segments
        self._orientation: Qt.Orientation = orientation  # Orientation of the battery

    @property
    def voltage(self) -> float:
        """float: The current voltage of the battery."""
        return self._voltage

    @voltage.setter
    def voltage(self, value: float) -> None:
        """Set the voltage of the battery and update the widget.

        Args:
            value (float): The new voltage value.
        """
        self._voltage = max(self._min_voltage, min(value, self._max_voltage))
        self.update()

    @property
    def min_voltage(self) -> float:
        """float: The minimum voltage of the battery."""
        return self._min_voltage

    @min_voltage.setter
    def min_voltage(self, value: float) -> None:
        """Set the minimum voltage and update the widget.

        Args:
            value (float): The new minimum voltage.
        """
        self._min_voltage = value
        self.update()

    @property
    def max_voltage(self) -> float:
        """float: The maximum voltage of the battery."""
        return self._max_voltage

    @max_voltage.setter
    def max_voltage(self, value: float) -> None:
        """Set the maximum voltage and update the widget.

        Args:
            value (float): The new maximum voltage.
        """
        self._max_voltage = value
        self.update()

    @property
    def segments(self) -> int:
        """int: The number of fill segments in the battery."""
        return self._segments

    @segments.setter
    def segments(self, value: int) -> None:
        """Set the number of segments and update the widget.

        Args:
            value (int): The new number of segments.
        """
        if value > 0:
            self._segments = value
            self.update()

    @property
    def orientation(self) -> Qt.Orientation:
        """Qt.Orientation: The orientation of the battery."""
        return self._orientation

    @orientation.setter
    def orientation(self, value: Qt.Orientation) -> None:
        """Set the orientation of the battery and update the widget.

        Args:
            value (Qt.Orientation): The new orientation (Qt.Horizontal or Qt.Vertical).
        """
        if value in (Qt.Horizontal, Qt.Vertical):
            self._orientation = value
            self.update()

    def paintEvent(self, event) -> None:
        """Override the paint event to draw the battery with segmented fill."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Define pen for drawing outlines
        pen_width = 2
        painter.setPen(QPen(Qt.black, pen_width))

        rect = self.rect()

        if self._orientation == Qt.Horizontal:
            self._draw_horizontal_battery(painter, rect, pen_width)
        elif self._orientation == Qt.Vertical:
            self._draw_vertical_battery(painter, rect, pen_width)

    def _draw_horizontal_battery(self, painter: QPainter, rect: QRect, pen_width: int) -> None:
        """Draw the battery in horizontal orientation.

        Args:
            painter (QPainter): The QPainter object.
            rect (QRect): The rectangle area of the widget.
            pen_width (int): The width of the pen.
        """
        battery_tip_width = rect.width() * 0.05  # 5% of width for the tip
        battery_body_width = rect.width() - battery_tip_width - pen_width
        battery_height = rect.height() - pen_width

        # Battery body rectangle
        body_rect = QRect(
            pen_width // 2,
            pen_width // 2,
            int(battery_body_width),
            int(battery_height),
        )
        painter.drawRect(body_rect)

        # Battery tip rectangle
        tip_x = body_rect.right() + 1
        tip_width = battery_tip_width
        tip_height = battery_height * 0.6
        tip_y = (rect.height() - tip_height) / 2
        tip_rect = QRect(
            tip_x,
            int(tip_y),
            int(tip_width),
            int(tip_height),
        )
        painter.drawRect(tip_rect)

        # Calculate number of filled segments
        fill_ratio = (
            (self._voltage - self._min_voltage)
            / (self._max_voltage - self._min_voltage)
            if self._max_voltage > self._min_voltage
            else 0.0
        )
        fill_ratio = max(0.0, min(fill_ratio, 1.0))
        filled_segments = floor(fill_ratio * self._segments)

        # Define padding and spacing
        padding = 4
        spacing = 4  # 2
        available_width = body_rect.width() - 2 * padding
        available_height = body_rect.height() - 2 * padding
        total_spacing = (self._segments - 1) * spacing
        segment_width = (
            (available_width - total_spacing) / self._segments
            if self._segments > 0
            else available_width
        )
        segment_height = available_height

        # Draw segments
        for i in range(self._segments):
            x = body_rect.left() + padding + i * (segment_width + spacing)
            y = body_rect.top() + padding
            segment_rect = QRect(
                int(x),
                int(y),
                int(segment_width),
                int(segment_height),
            )
            if i < filled_segments:
                painter.fillRect(segment_rect, QColor(0, 200, 0))  # Green color
            else:
                painter.fillRect(
                    segment_rect, QColor(220, 220, 220)
                )  # Light gray for empty segments
            painter.drawRect(segment_rect)

    def _draw_vertical_battery(self, painter: QPainter, rect: QRect, pen_width: int) -> None:
        """Draw the battery in vertical orientation.

        Args:
            painter (QPainter): The QPainter object.
            rect (QRect): The rectangle area of the widget.
            pen_width (int): The width of the pen.
        """
        battery_tip_height = rect.height() * 0.05  # 5% of height for the tip
        battery_body_height = rect.height() - battery_tip_height - pen_width
        battery_width = rect.width() - pen_width

        # Battery tip rectangle (positioned at the top)
        tip_x = (rect.width() - battery_width * 0.6) / 2
        tip_y = pen_width // 2
        tip_width = battery_width * 0.6
        tip_height = battery_tip_height
        tip_rect = QRect(
            int(tip_x),
            tip_y,
            int(tip_width),
            int(tip_height),
        )
        painter.drawRect(tip_rect)

        # Battery body rectangle (positioned below the tip)
        body_rect = QRect(
            pen_width // 2,
            pen_width // 2 + int(battery_tip_height),
            int(battery_width),
            int(battery_body_height),
        )
        painter.drawRect(body_rect)

        # Calculate number of filled segments
        fill_ratio = (
            (self._voltage - self._min_voltage)
            / (self._max_voltage - self._min_voltage)
            if self._max_voltage > self._min_voltage
            else 0.0
        )
        fill_ratio = max(0.0, min(fill_ratio, 1.0))
        filled_segments = floor(fill_ratio * self._segments)

        # Define padding and spacing
        padding = 4
        spacing = 4  # 2
        available_width = body_rect.width() - 2 * padding
        available_height = body_rect.height() - 2 * padding
        total_spacing = (self._segments - 1) * spacing
        segment_height = (
            (available_height - total_spacing) / self._segments
            if self._segments > 0
            else available_height
        )
        segment_width = available_width

        # Draw segments from bottom to top
        for i in range(self._segments):
            x = body_rect.left() + padding
            # Calculate y starting from the bottom
            y = body_rect.bottom() - padding - (i + 1) * (segment_height + spacing) + spacing
            segment_rect = QRect(
                int(x),
                int(y),
                int(segment_width),
                int(segment_height),
            )
            if i < filled_segments:
                painter.fillRect(segment_rect, QColor(0, 200, 0))  # Green color
            else:
                painter.fillRect(
                    segment_rect, QColor(220, 220, 220)
                )  # Light gray for empty segments
            painter.drawRect(segment_rect)

    def sizeHint(self) -> QSize:
        """Provide a recommended size for the widget.

        Returns:
            QSize: Recommended width and height.
        """
        return QSize(200, 100)


class BatteryWidgetDemo(QWidget):
    """Demo application to showcase the BatteryWidget with 
    segmented fill and orientation control."""

    def __init__(self) -> None:
        """Initialize the demo application."""
        super().__init__()

        self.min_voltage = 0.0
        self.max_voltage = 5.0
        self.segments = 10

        self.battery_widget_horizontal = None
        self.battery_widget_horizontal_label = None
        self.battery_widget_vertical = None
        self.battery_widget_vertical_label = None
        self.slider = None

        self.initUI()    

    def initUI(self) -> None:
        """Initialize the user interface."""  

        # Initialize the BatteryWidget with desired number of segments and default orientation
        self.battery_widget_horizontal = BatteryWidget(self, 
                                                       segments=self.segments, 
                                                       min_voltage=self.min_voltage,
                                                       max_voltage=self.max_voltage,
                                                       orientation=Qt.Horizontal)
        self.battery_widget_horizontal.setFixedSize(250, 100)

        # Label to display current voltage
        self.battery_widget_horizontal_label = QLabel("Voltage: 0V")
        self.battery_widget_horizontal_label.setAlignment(Qt.AlignCenter)

        # Initialize the BatteryWidget with desired number of segments and default orientation
        self.battery_widget_vertical = BatteryWidget(self, 
                                                     segments=self.segments, 
                                                     min_voltage=self.min_voltage,
                                                     max_voltage=self.max_voltage,
                                                     orientation=Qt.Vertical)
        self.battery_widget_vertical.setFixedSize(100, 250)

        # Label to display current voltage
        self.battery_widget_vertical_label = QLabel("Voltage: 0V")
        self.battery_widget_vertical_label.setAlignment(Qt.AlignCenter)

        # Create a slider to simulate voltage changes
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.segments)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.updateVoltage)        

        battery_widget_horizontal_layout = QVBoxLayout()
        battery_widget_horizontal_layout.addStretch(1)
        battery_widget_horizontal_layout.addWidget(self.battery_widget_horizontal)
        battery_widget_horizontal_layout.addWidget(self.battery_widget_horizontal_label)
        battery_widget_horizontal_layout.addStretch(1)

        battery_widget_vertical_layout = QVBoxLayout()
        battery_widget_vertical_layout.addStretch(1)
        battery_widget_vertical_layout.addWidget(self.battery_widget_vertical)
        battery_widget_vertical_layout.addWidget(self.battery_widget_vertical_label)
        battery_widget_vertical_layout.addStretch(1)

        #
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addLayout(battery_widget_horizontal_layout)
        layout.addStretch(1)
        layout.addLayout(battery_widget_vertical_layout)
        layout.addStretch(1)

        # Layout setup
        main_layout = QVBoxLayout() 
        main_layout.addStretch(1)       
        main_layout.addLayout(layout)
        main_layout.addStretch(1)
        main_layout.addWidget(self.slider)

        self.setLayout(main_layout)
        self.setFixedSize(800, 400)
        self.setWindowTitle("Battery Widget Demo")


    def updateVoltage(self, value: int) -> None:
        """Update the voltage of the battery widget and label.

        Args:
            value (int): The new voltage value from the slider.
        """
        
        steps = self.max_voltage / self.segments        
        voltage = value * steps

        self.battery_widget_horizontal.voltage = float(voltage)
        self.battery_widget_horizontal_label.setText(f"Voltage: {voltage:.2f}V")

        # text = f"{self.value:.2f}

        self.battery_widget_vertical.voltage = float(voltage)
        self.battery_widget_vertical_label.setText(f"Voltage: {voltage:.2f}V")


def main():
    """Run the BatteryWidget demo application."""
    app = QApplication(sys.argv)
    demo = BatteryWidgetDemo()
    demo.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
