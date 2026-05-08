# Dormitory #14 to Lviv Polytechnic National University (Building 4) shortest route.

Personal project that visualizes the shortest route from Dormitory #14 to Lviv Polytechnic National University (Building 4).

## What it does
- Builds the transport / landmark graph from the hard-coded edges in `main.py`
- Finds the weighted shortest path with `networkx`
- Renders a polished PNG visualization to `graph_visualization.png`
- Uses color, labels, and a legend to make the graph easy to read

## Theory used
- Basic graph theory for simple weighted graphs
- Djikstra's algorithm (modified for weighted graphs) to find the shortest path. 
I used this algorithm because of it's simplicity and efficiency for this type of problem.
As long as weights are positive, Djikstra's algorithm is guaranteed to find the shortest path.
- Used Tobler's function to calculate the average velocity of the person walking based on slope of the path.
Tobler's velocity formula (in meters per second):
\begin{equation}
    V = 6 \cdot e^{-3.5 \cdot |S + 0.05|}
\end{equation}
Where:
\( V \) is the walking velocity in meters per second.
\( S \) is the slope of the path, calculated as the change in elevation divided by the horizontal distance.
\( -0.05 \) offset represents a slight downward slope of approximately 5% where hikers achieve their maximum speed.
- Actual formula for weights i've used:
\begin{equation}
w = \frac{d}{\frac{6 \cdot e^{(-3.5 \cdot |s + 0.05|)}}{3.6}} + \sum_{i=1}^{n}c_i
\end{equation}
Where \( d \) is the distance between the two points, \( s \) is the slope of the path, and \( c_i \) are the additional costs for the path (e.g., traffic, safety, etc.). 
The division by 3.6 converts the velocity from meters per second to kilometers per hour.

## Run it

```bash
python3 main.py
```

## Dependencies

Install packages with:

```bash
pip install -r requirements.txt
```

## Output

After running the script, check the generated image:

- `graph_visualization.png`

