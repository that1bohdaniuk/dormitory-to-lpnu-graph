[English](#english) | [Українська](#українська)

<a id="english"></a>
# Shortest Route: Dormitory 14 to Lviv Polytechnic

A personal project visualizing the optimal pedestrian route from Dormitory #14 to Lviv Polytechnic National University (Building 4) using spatial network analysis.

## Features
* **Graph Construction:** Builds a transport and landmark graph using defined edges in `main.py`.
* **Routing:** Calculates the weighted shortest path using `networkx`.
* **Visualization:** Renders a polished, color-coded PNG (`graph_visualization.png`) complete with labels and a legend for readability.

## Theoretical Background

### Shortest Path Algorithm
This project uses **Dijkstra's Algorithm** to evaluate the graph. Because all physical edge weights (representing time) are strictly positive, Dijkstra's is mathematically guaranteed to find the optimal shortest path efficiently.

### Edge Weight Calculation (Time Cost)
Edge weights represent the total traversal time in seconds. The formula combines physical movement time—derived from **Tobler's Hiking Function**—with discrete obstacle penalties.

**Tobler's Velocity Formula:**
Tobler's function calculates the walking speed based on the path's slope:

$$V = 6 \cdot e^{-3.5 \cdot |s + 0.05|}$$

*   **$V$**: Walking velocity in **km/h**.
*   **$s$**: Slope of the path (change in elevation divided by horizontal distance).
*   **$-0.05$**: An offset accounting for the biomechanical reality that hikers achieve maximum speed at a slight downward grade of approximately 5%.

**Total Edge Weight Formula:**
To calculate the total time weight in seconds, we apply the velocity to the distance and add penalties:

$$w = \frac{d}{\frac{6 \cdot e^{(-3.5 \cdot |s + 0.05|)}}{3.6}} + \sum_{i=1}^{n}c_i$$

*   **$w$**: Total edge weight (time in seconds).
*   **$d$**: Distance between the two points in meters.
*   **$c_i$**: Additional fixed time costs in seconds (e.g., waiting at traffic lights, crossing safety delays).
*   *Note:* The Tobler formula yields km/h. Dividing the denominator by **3.6** converts this velocity to **m/s**. Dividing the distance ($d$) by this m/s velocity gives the base time in seconds.

## Installation

Ensure you have Python installed, then install the required dependencies:

```bash
pip install -r requirements.txt
