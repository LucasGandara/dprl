# DPRL - Deep Reinforcement Learning Toolkit

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A comprehensive reinforcement learning toolkit featuring state-of-the-art algorithms for both Gymnasium environments and custom-built environments, complete with a powerful command-line interface.

## 🚀 Features

- **Multiple RL Algorithms**: Implementation of popular reinforcement learning algorithms
- **Gymnasium Integration**: Full support for OpenAI Gymnasium environments
- **Custom Environments**: Built-in custom environments for specialized training scenarios
- **CLI Interface**: Easy-to-use command-line interface powered by Click
- **Extensible Architecture**: Modular design for easy algorithm and environment extension
- **Training Utilities**: Comprehensive training, evaluation, and visualization tools

## 📦 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/LucasGandara/dprl.git
cd dprl

# Install in development mode
pip install -e .
```

### Prerequisites

- Python 3.13 or higher
- pip package manager

## 🎯 Quick Start

### Command Line Interface

DPRL comes with a powerful CLI that makes it easy to train and evaluate reinforcement learning agents:

```bash
# Train an agent on CartPole environment
dprl train --algorithm dqn --env CartPole-v1 --episodes 1000

# Evaluate a trained model
dprl evaluate --model path/to/model.pkl --env CartPole-v1 --episodes 100

# List available algorithms
dprl list-algorithms

# List available environments
dprl list-environments

# Get help
dprl --help
```

### Python API

```python
import dprl
from dprl.algorithms import DQN
from dprl.environments import make_env

# Create environment
env = make_env('CartPole-v1')

# Initialize algorithm
agent = DQN(env.observation_space, env.action_space)

# Train the agent
agent.train(env, episodes=1000)

# Evaluate performance
rewards = agent.evaluate(env, episodes=100)
print(f"Average reward: {sum(rewards) / len(rewards):.2f}")
```

## 🧠 Supported Algorithms

### Value-Based Methods
- **DQN** (Deep Q-Network)
- **Double DQN**
- **Dueling DQN**
- **Rainbow DQN**

### Policy-Based Methods
- **REINFORCE**
- **Actor-Critic**
- **PPO** (Proximal Policy Optimization)
- **A2C** (Advantage Actor-Critic)

### Model-Based Methods
- **MCTS** (Monte Carlo Tree Search)
- **Dyna-Q**

## 🎮 Supported Environments

### Gymnasium Environments
- Classic Control (CartPole, MountainCar, Acrobot, etc.)
- Atari Games (Breakout, Pong, Space Invaders, etc.)
- Box2D (LunarLander, BipedalWalker, etc.)
- MuJoCo (Ant, Humanoid, Walker2d, etc.)

### Custom Environments
- Grid World variants
- Multi-agent scenarios
- Custom control problems

## 🛠️ CLI Commands

### Training
```bash
dprl train [OPTIONS]

Options:
  --algorithm, -a TEXT     Algorithm to use [required]
  --env, -e TEXT          Environment name [required]
  --episodes INTEGER      Number of training episodes [default: 1000]
  --learning-rate FLOAT   Learning rate [default: 0.001]
  --batch-size INTEGER    Batch size for training [default: 32]
  --save-path TEXT        Path to save the trained model
  --config TEXT           Path to configuration file
  --verbose, -v           Enable verbose output
```

### Evaluation
```bash
dprl evaluate [OPTIONS]

Options:
  --model, -m TEXT        Path to trained model [required]
  --env, -e TEXT          Environment name [required]
  --episodes INTEGER      Number of evaluation episodes [default: 100]
  --render                Render episodes during evaluation
  --save-video TEXT       Save evaluation videos to directory
```

### Utilities
```bash
# List available algorithms
dprl list-algorithms

# List available environments  
dprl list-environments

# Show algorithm details
dprl info --algorithm dqn

# Show environment details
dprl info --environment CartPole-v1
```

## 📊 Configuration

DPRL supports configuration via YAML files for reproducible experiments:

```yaml
# config.yaml
algorithm:
  name: "dqn"
  learning_rate: 0.001
  batch_size: 32
  memory_size: 10000
  epsilon_decay: 0.995

environment:
  name: "CartPole-v1"
  max_steps: 500

training:
  episodes: 1000
  save_frequency: 100
  evaluation_frequency: 50

logging:
  tensorboard: true
  wandb: false
```

Use configuration files with:
```bash
dprl train --config config.yaml
```

## 📈 Monitoring and Visualization

- **TensorBoard Integration**: Real-time training metrics visualization
- **Weights & Biases Support**: Experiment tracking and comparison
- **Custom Plotting**: Built-in plotting utilities for performance analysis

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/LucasGandara/dprl.git
cd dprl
pip install -e ".[dev]"

# Run tests
python -m unittest discover tests

# Run linting
flake8 dprl/
black dprl/
```

## 📚 Documentation

- [API Documentation](docs/api.md)
- [Algorithm Implementations](docs/algorithms.md)
- [Custom Environments](docs/environments.md)
- [Examples and Tutorials](examples/)

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**: Make sure all dependencies are installed
   ```bash
   pip install -e ".[all]"
   ```

2. **Gymnasium Environment Issues**: Update gymnasium to the latest version
   ```bash
   pip install gymnasium[all] --upgrade
   ```

3. **CUDA/GPU Issues**: Ensure proper PyTorch installation for your system
   ```bash
   # For CUDA 11.8
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
   ```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI Gymnasium team for the environment standards
- Stable Baselines3 for algorithm inspiration
- Click team for the excellent CLI framework

## 📬 Contact

- **Author**: Lucas Gandara
- **Email**: [your-email@example.com]
- **GitHub**: [@LucasGandara](https://github.com/LucasGandara)

---

⭐ **Star this repository if you found it helpful!**