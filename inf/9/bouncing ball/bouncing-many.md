# Bouncing Balls

## User stories

### [x] Single ball, traveling across the screen, bouncing from the edges
- 5 CU (starting point, see [single bouncing ball](./bouncing-single.md)

### [x] Multiple balls (up to 100?), each behaving like the single ball
- [x] different color and size for each ball
- [x] different starting position and velocity for each ball


## Design considerations

### Requirements (changes)
- Starting point: [single bouncing ball requirements](./bouncing-single.md#Requirements)
- Extend `Ball` structure to `Balls`, containing several balls

### Data design
- Option A: make a list of balls, e.g.:
  ```
  single_ball = Ball()
  many_balls = [Ball(), Ball(), Ball(), ...]
  ```

- Option B: change `Ball` to `Balls`, to contain _all_ balls at once
  ```
  single_ball = Ball()
  many_balls = Balls()
  ```
  - keep fields as in [previous version](./bouncing-single.md)
  - BUT: extend each field to contain an extra dimension

- Choice: go for option B, because it is the "natural" data
  representation for multiple-instance graphical objects

### Flow design
After initialization, the application repeatedly runs one single loop:
```mermaid
flowchart MainLoop
A[Handle incoming user input] --> B[Update ball position]
B --> C[Display ball]
C --> D[Wait for period]
```
  
## Project management considerations

### Tasks and complexity estimation

- [x] 1 CU: extend `Ball` into `Balls` (keep the rest the same,
  hold all the data as if we had many balls, but only work with
  the 1st ball of the data)
  
- [x] 5 CU: add an extra number of balls to the game's `Balls`
  structure; only update the 1st ball when calculating new position,
  but display _all_ balls on every iteration (all _other_ balls
  will not move at first)
  
- [x] 5 CU: make all balls update position ("move") on every
  iteration
  
- [ ] 5 CU: optimizations using `numpy` array calculations?
