import os

import gymnasium
import pygame

from .base import Base
from .bird import Bird
from .pipe import Pipe

pygame.init()
pygame.font.init()


class FlappyBird(gymnasium.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}
    FLOOR = 730  # y pos of floor

    def __init__(self, render_mode=None, draw_lines=False):
        """
        Initialize the environment
        :param render_mode: the mode to render with
        """
        self.draw_lines = draw_lines
        self.font = pygame.font.SysFont("comicsans", 50)
        self.render_mode = render_mode
        self.screen_width = 500
        self.screen_height = 800
        self.background_img = pygame.transform.scale2x(
            pygame.image.load(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "assets",
                    "imgs",
                    "bg.png",
                )
            )
        )
        self.score = 0
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.observation_space = gymnasium.spaces.Dict(
            {
                "bird": gymnasium.spaces.Box(low=0, high=self.screen_height, dtype=int),
                "pipe_top": gymnasium.spaces.Box(
                    low=0, high=self.screen_height, dtype=int
                ),
                "pipe_bottom": gymnasium.spaces.Box(
                    low=0, high=self.screen_height, dtype=int
                ),
                "pipe_x": gymnasium.spaces.Box(
                    low=0, high=self.screen_width, dtype=int
                ),
            }
        )

        # Define action and observation space
        # We have 2 actions, to swing or not to swing
        self.action_space = gymnasium.spaces.Discrete(2)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        self.bird = Bird(230, 350, self.screen)
        self.base = Base(self.FLOOR)
        self.pipes = [Pipe(700)]
        self.pipe_ind = 0

    def get_observation(self):
        """
        Get the current observation of the environment
        :return: observation (object): the current observation of the space.
        """
        return [
            self.bird.y,
            abs(self.bird.y - self.pipes[self.pipe_ind].height),
            abs(self.bird.y - self.pipes[self.pipe_ind].bottom),
            self.pipes[self.pipe_ind].x,
        ]

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        :return: observation (object): the initial observation of the space.
        """
        self.bird = Bird(230, 350, self.screen)
        self.pipes = [Pipe(700)]
        self.pipe_ind = 0
        self.score = 0
        return self.get_observation(), {}

    def step(self, action):
        """
        The agent takes a step in the environment
        :param action: an action provided by the agent
        :return: observation, reward, done, info
        """
        done = False
        reward = 1

        self.bird.step(action)
        self.base.move()

        for pipe in self.pipes:
            pipe.move()
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                self.pipes.remove(pipe)

            if not pipe.passed and pipe.x < self.bird.x:
                reward += 100
                pipe.passed = True
                self.pipes.append(Pipe(700))

            done = pipe.collide(self.bird)

            if (
                self.bird.y + self.bird.img.get_height() - 10 >= self.FLOOR
                or self.bird.y < -50
            ):
                done = True
                reward = -1

        if self.render_mode == "human":
            self.render()
            self.clock.tick(30)

        self.score += reward
        return self.get_observation(), reward, done, {}, {}

    def render(self):
        """
        Render the environment to the screen
        :return: None
        """

        # Draw the screen
        self.screen.fill((0, 0, 0))  # Fill the screen with black
        self.screen.blit(self.background_img, (0, 0))  # Draw the background
        self.base.draw(self.screen)  # Draw the floor

        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)
        score_label = self.font.render("Score: " + str(self.score), 1, (255, 255, 255))
        self.screen.blit(
            score_label, (self.screen_width - score_label.get_width() - 10, 10)
        )
        if self.draw_lines:
            try:
                pygame.draw.line(
                    self.screen,
                    (255, 0, 0),
                    (
                        self.bird.x + self.bird.img.get_width() / 2,
                        self.bird.y + self.bird.img.get_height() / 2,
                    ),
                    (
                        self.pipes[self.pipe_ind].x
                        + self.pipes[self.pipe_ind].PIPE_TOP.get_width() / 2,
                        self.pipes[self.pipe_ind].height,
                    ),
                    5,
                )
                pygame.draw.line(
                    self.screen,
                    (255, 0, 0),
                    (
                        self.bird.x + self.bird.img.get_width() / 2,
                        self.bird.y + self.bird.img.get_height() / 2,
                    ),
                    (
                        self.pipes[self.pipe_ind].x
                        + self.pipes[self.pipe_ind].PIPE_BOTTOM.get_width() / 2,
                        self.pipes[self.pipe_ind].bottom,
                    ),
                    5,
                )
            except:
                pass

        pygame.event.pump()
        pygame.display.update()


if __name__ == "__main__":
    env = FlappyBird(render_mode="human", draw_lines=True)
    env.reset()

    # Alternate 5 frames of action 0 with 5 frames of action 1, repeatedly
    action = 0
    frames_per_action = 20
    action_frame_count = 0

    while True:
        # Handle events
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

        # Step environment with the current action
        observation, reward, done, info = env.step(action)
        if done:
            break

        # Count frames for the current action and flip after N frames
        action_frame_count += 1
        if action_frame_count >= frames_per_action:
            action = 1 - action  # toggle between 0 and 1
            action_frame_count = 0

        # Render at the chosen FPS
        env.render()
        env.clock.tick(30)
