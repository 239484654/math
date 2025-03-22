# Simple-Calculator for Windows
## Introduction
This calculator is a simple desktop application designed to provide users with basic calculation functions. It draws on the design concepts and ideas of some open-source projects and features simplicity and ease of use.

[Chinese version](./README_zhs.md)

## Function Overview
This calculator has the following main functions:
1. **Basic Operations**: Supports basic mathematical operations such as addition, subtraction, multiplication, and division.
2. **Decimal Handling**: Can handle the input and calculation of numbers containing decimal points.
3. **Number Input**: Users can input numbers by clicking the number buttons on the interface.
4. **Clear Operations**: Provides functions to clear all input, clear the current input, and delete the last digit.
5. **System Color Adaptation**: Can automatically adjust the interface color according to the system's theme color (dark or light).

## Interface Description
### Color Mode
The calculator will automatically switch the interface color according to the system's color theme. If the system is in dark mode, the calculator will adopt a dark color scheme; if it is in light mode, it will use a light color scheme.

### Display Area
- **Current Display**: Used to display the numbers entered by the user and the calculation results. The maximum display length is 10 digits.

### Button Area
- **Number Buttons**: From 0 to 9, used for entering numbers.
- **Decimal Point Button**: Used for entering decimal points.
- **Operator Buttons**: Including operators such as addition (+), subtraction (-), multiplication (×), and division (÷), used for performing mathematical operations.
- **Clear Buttons**:
  - **Clear All**: Clears all input and calculation results, and resets the display area to 0.
  - **Clear Current**: Clears the currently entered number.
  - **Delete One**: Deletes the last digit in the display area.

## Usage Method
### Number Input
Click the number buttons (0 - 9) to enter numbers. If you need to enter a decimal number, you can click the decimal point button.

### Basic Operations
After entering the first number, click the operator button to select the operation to be performed, then enter the second number, and finally click the equal sign (=) button to perform the calculation. The calculation result will be displayed in the display area.

### Clear Operations
- If you want to clear all input and calculation results, click the "Clear All" button.
- If you only want to clear the currently entered number, click the "Clear Current" button.
- If you want to delete the last digit in the display area, click the "Delete One" button.

## Technical Details
### Dependent Libraries
This calculator uses the following Python libraries:
- `math`: Used for mathematical calculations.
- `tkinter`: Used for creating graphical user interfaces (GUIs).
- `cmath`: Used for complex number calculations.
- `fractions`: Used for fraction handling.
- `decimal`: Used for high-precision decimal calculations.
- `threading`: Used for starting a thread to check the system color.
- `time`: Used for time-related operations.
- `darkdetect`: Used for detecting the system's color theme (dark or light).

### Code Structure
- `add_fraction`: Used to handle the addition operation of fractions.
- `calculate_expression`: Used to calculate the entered expression.
- `Int`: Used for integer conversion.
- `pressNumber`: Handles the click event of the number buttons.
- `pressDP`: Handles the click event of the decimal point button.
- `clearAll`: Clears all input and calculation results.
- `clearCurrent`: Clears the currently entered number.
- `delOne`: Deletes the last digit in the display area.
- `modifyResult`: Modifies the calculation result.
- `pressOperator`: Handles the click event of the operator buttons.
- `Demo`: Used for demonstration.
- `check_system_color`: Starts a thread to check the system's color theme and adjusts the interface color according to the result.

## Citation Instructions
This project refers to the following open-source projects:
- [Cascadia Code](https://github.com/microsoft/cascadia-code/releases)
- [Microsoft Calculator](https://github.com/Microsoft/calculator)

These projects have provided us with valuable inspiration and references, and we would like to express our gratitude here.

## Notes
- The maximum length of the display area is 10 digits, and numbers that are too long may not be fully displayed.
- If the `darkdetect` library is not installed in the system, the calculator will default to light mode.

We hope this instruction document can help you use this calculator better. If you have any questions or suggestions, please feel free to provide feedback. 