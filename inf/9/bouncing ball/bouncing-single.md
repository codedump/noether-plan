# Bouncing Balls

## User stories

### [x] Single ball, traveling across the screen, bouncing from the edges
- [x] Display red ball at random position on the screen
- [x] Random size (radius)
- [x] Periodic screen update (60 FPS)
- [x] Ball should have velocities assigned (random,
  in each direction)
- [x] On each iteration, update ball position according to
  velocities
- [x] "Bounce off" screen edges (change direction every time
  it touches the edge). Consider ball size when bouncing


## Design considerations

### Requirements
- Use designated structure for ball
- Use designated structure for "the game"
- Keep game data and display data separate

### Data design
- One `GameData` structure (object) for generic game data
  (timing, runtime data)
  ```
  @startuml
  object GameData
  GameData:running=True
  GameData:period=1/60
  GameData:ball=Ball()
  @enduml
  ```

- Keep ball state in a specific structure `Ball`; necesssary
  fields:
  - `pos`: position (x, y) of the ball
  - `vel`: velocity (Vx, Vy), in pixels/second
  - `rad`: "size" of the ball, i.e. radius
  - `rgb`: color of the ball as RGB tuple
  ```
  @startuml
  object Ball
  Ball:pos=(x, y)
  Ball:vel=(Vx, Vy)
  Ball:rad=42
  Ball:rgb=[128, 0, 0]
  ```

- Use `array()` as basic structure wherever similar data
  are going to be processed at once (e.g. coordinates: there
  are two directions).
  We don't use `list()` because `list()` will inevitably get
  slow (wrong data container paradigm)


## Project management considerations

- Project serves as example of "complexity".
  We define this project to have complexity of 5 CU
  ("complexity units").
