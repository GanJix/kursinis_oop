# Coursework Report: Accelerometer Data Processor

## 1. Introduction

### Application Overview

**Accelerometer Data Processor** Šios programos esmė yra gautus duomenis .csv faile atvaizduoti grafike, duomenims pritaikant įvairius filtrus. Duomenys yra gaunami iš specialaus aparato kuriame yra įdetas lazeris kuris yra purtomas taip yra lazeris kalibruojamas, testuojamas jo ilgaamžiškumas ir jautrumas purtymams. Lazeris aparate yra purtomas x, y , z ašimis ir taip įmituojant pvz. jo tranportavimo drebejimus ir pns.  ir rodoma kiek g force sensorius patiria kiekviena ašimi. Tada atlikus Furje transformaciją gaunamas signalas yra paverčiamas dažnio spektru, grafikuose galima pamatyti kiek daug ir kaip itensyviai buvo purtoma kuriame dažnyje. Taip pat grafikai atvaizduoja kiek energijos tenkam kuriam dažniui.

### How to Run the Program

Ensure you have the following Python libraries installed: pandas, numpy, matplotlib, scipy, tkinter.

You can install missing packages via pip, for example:
**pip install pandas numpy matplotlib scipy**
Place the CSV file MSR457988x_250314_163216.csv (or any properly formatted accelerometer CSV data file) in the same directory as the Python script.

Run the program by executing:
**python main_code_oop.py**

### How to Use the Program

Upon running, a window with buttons appears.

Click X-axis Acc, Y-axis Acc, or Z-axis Acc to plot acceleration data along that axis.

Click All Axes Acc to plot acceleration data from all three axes on one graph.

Click FFT of Z-axis to perform and display the frequency spectrum analysis of the Z-axis acceleration data.

The plots will appear in separate windows.


  

## 2. Body/Analysis

### Code Structure

My application is written in one python script: 

- **main_code.py**

### Object-Oriented Programming (OOP) Pillars

1. **Encapsulation**
Data and methods related to plotting behavior are encapsulated inside classes. For example, the AccelerometerApp class encapsulates the GUI logic and data loading:
   
    ```python
    class AccelerometerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Accelerometer Data Processor")
        # Initialization of buttons and loading data
        self.data = self.load_data('MSR457988x_250314_163216.csv')

    def load_data(self, filename):
        # Reads and preprocesses the CSV accelerometer data
        # Returns time and acceleration arrays for X, Y, Z axes
    ```

   **Encapsulation** The internal state (self.data) and GUI components are private to the class and accessed only via methods.

   

2. **Inheritance:** An abstract base class GraphStrategy defines the interface for plotting strategies. Concrete graph classes inherit and override the plot method:


    ```python
    class GraphStrategy:
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        raise NotImplementedError("Subclasses should implement this!")

    class XAxisGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        plt.plot(relative_time, acc_x)
        plt.title('X-axis Acceleration')
        plt.show()

   ```

   This **inheritance** allows code reuse and polymorphic behavior.
    


3. **Polymorphism:** The GraphContext class uses polymorphism to handle multiple plotting strategies uniformly:
   

	```python
    class GraphContext:
    def __init__(self, strategy: GraphStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: GraphStrategy):
        self._strategy = strategy

    def plot(self, relative_time, acc_x, acc_y, acc_z):
        self._strategy.plot(relative_time, acc_x, acc_y, acc_z)

    ```
  
Here, plot() calls the appropriate subclass’s implementation depending on the current strategy object.


4. **Abstraction** The program abstracts plotting details from the GUI. The user interacts with button commands that internally delegate plotting to strategy classes:



   	```python
    def plot_x_axis(self):
    context = GraphContext(XAxisGraph())
    context.plot(self.data[0], self.data[1], self.data[2], self.data[3])


    ```
   

   The GUI code does not need to know how plotting works internally; it only calls plot() on the context.
   

### Design patterns

The **Strategy Pattern** is used to select different graph plotting behaviors dynamically. This fits the program's requirement to plot different graph types (single axis, all axes, FFT) while maintaining a clean, modular design.

Example of the Strategy base class and concrete subclasses:
```python
class GraphStrategy:
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        raise NotImplementedError("Subclasses should implement this!")

class XAxisGraph(GraphStrategy):
    def plot(self, relative_time, acc_x, acc_y, acc_z):
        plt.figure(figsize=(8, 6))
        plt.plot(relative_time, acc_x, 'r', linewidth=1.5)
        plt.xlabel('Time (s)')
        plt.ylabel('Acceleration (G)')
        plt.title('X-axis Acceleration')
        plt.grid(True)
        plt.show()

```
Usage of the **Strategy Pattern** via GraphContext in the application:
```python
class GraphContext:
    def __init__(self, strategy: GraphStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: GraphStrategy):
        self._strategy = strategy

    def plot(self, relative_time, acc_x, acc_y, acc_z):
        self._strategy.plot(relative_time, acc_x, acc_y, acc_z)

```

### Composition / aggregation
The AccelerometerApp class aggregates plotting strategies by creating and using GraphContext objects that use different GraphStrategy subclasses to display the data. This demonstrates the use of composition/aggregation principles, as the app "has a" context and strategies to perform different tasks without inheriting from them.

For example, in the button command methods, AccelerometerApp creates a GraphContext object with a specific plotting strategy and then calls its plot() method. This shows that AccelerometerApp “has a” GraphContext and “uses” different GraphStrategy subclasses without inheriting from them:

```python
def plot_x_axis(self):
    # Composition: creates GraphContext with XAxisGraph strategy
    context = GraphContext(XAxisGraph())
    # Delegates plotting to the strategy via context
    context.plot(self.data[0], self.data[1], self.data[2], self.data[3])

def plot_all_axes(self):
    # Aggregation: uses a different strategy for plotting all axes
    context = GraphContext(AllAxesGraph())
    context.plot(self.data[0], self.data[1], self.data[2], self.data[3])

```
This illustrates **aggregation** because:

AccelerometerApp holds references to the GraphContext objects (created on demand).

GraphContext holds references to specific strategy objects (XAxisGraph, AllAxesGraph, etc.).

They collaborate by passing data and delegating tasks, maintaining loose coupling and modularity.

### Writing to File

The program reads accelerometer data from a CSV file (MSR457988x_250314_163216.csv) using the Pandas library.

Data reading includes parsing timestamps and acceleration values on the X, Y, and Z axes, cleaning invalid data.

Example of reading and preparing data:


```python
def load_data(self, filename):
    data = pd.read_csv(filename, delimiter=';', engine='python', skiprows=4)
    
    time_column = data.columns[0]
    time_str = data[time_column] 
    time_parsed = pd.to_datetime(time_str, format='%Y-%m-%d %H:%M:%S.%f', errors='coerce')
    time_seconds = (time_parsed - time_parsed.iloc[0]).dt.total_seconds()

    acc_x = pd.to_numeric(data.iloc[:, 1], errors='coerce')
    acc_y = pd.to_numeric(data.iloc[:, 2], errors='coerce')
    acc_z = pd.to_numeric(data.iloc[:, 3], errors='coerce')

    valid_data = ~acc_x.isna() & ~acc_y.isna() & ~acc_z.isna()
    time_seconds = time_seconds[valid_data]
    acc_x = acc_x[valid_data]
    acc_y = acc_y[valid_data]
    acc_z = acc_z[valid_data]

    return time_seconds, acc_x, acc_y, acc_z

```




## 3. Results and Summary

### Results

Successfully implemented a modular Python application for accelerometer data visualization.

Demonstrated effective use of OOP principles and the Strategy design pattern.

Provided a user-friendly GUI with buttons to select and display different graph types.

Parsed complex CSV data with timestamps into usable numerical formats.

### Conclusions

The coursework fulfilled all the required functional and design requirements.

Using OOP and design patterns improved code organization, allowing easy extension (e.g., adding new plotting strategies).

Future work could include adding file export functionality, real-time data streaming support, and unit tests for robustness.

