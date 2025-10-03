"""
Environment utilities for deep reinforcement learning.

This module provides utilities for creating, wrapping, and managing RL environments.
"""

import gymnasium as gym
from typing import Optional, Dict, Any
import numpy as np


def make_env(env_name: str, render: bool = False, **kwargs) -> gym.Env:
    """
    Create and configure an environment.
    
    Args:
        env_name: Name of the environment (e.g., 'CartPole-v1')
        render: Whether to enable rendering
        **kwargs: Additional environment parameters
        
    Returns:
        Configured environment instance
    """
    try:
        # Set render mode
        render_mode = None
        if render:
            render_mode = kwargs.get('render_mode', 'human')
        
        # Create the environment
        env = gym.make(env_name, render_mode=render_mode, **kwargs)
        
        # Apply common wrappers if needed
        env = apply_wrappers(env, env_name)
        
        return env
        
    except gym.error.Error as e:
        raise ValueError(f"Environment '{env_name}' not found: {e}")


def apply_wrappers(env: gym.Env, env_name: str) -> gym.Env:
    """
    Apply common wrappers to the environment.
    
    Args:
        env: Base environment
        env_name: Environment name for wrapper selection
        
    Returns:
        Wrapped environment
    """
    # Add environment-specific wrappers here
    
    # Example: Apply observation normalization for continuous control tasks
    if any(name in env_name.lower() for name in ['pendulum', 'mountaincar', 'acrobot']):
        env = NormalizeObservation(env)
    
    # Example: Apply action clipping for continuous action spaces
    if hasattr(env.action_space, 'high'):
        env = ClipAction(env)
    
    return env


class NormalizeObservation(gym.ObservationWrapper):
    """Normalize observations to have zero mean and unit variance."""
    
    def __init__(self, env, epsilon=1e-8):
        """
        Initialize the wrapper.
        
        Args:
            env: Environment to wrap
            epsilon: Small value to avoid division by zero
        """
        super().__init__(env)
        self.epsilon = epsilon
        self.obs_rms = RunningMeanStd(shape=self.observation_space.shape)
    
    def observation(self, observation):
        """Normalize the observation."""
        self.obs_rms.update(observation)
        return (observation - self.obs_rms.mean) / np.sqrt(self.obs_rms.var + self.epsilon)


class ClipAction(gym.ActionWrapper):
    """Clip actions to the valid range."""
    
    def __init__(self, env):
        """Initialize the wrapper."""
        super().__init__(env)
        
    def action(self, action):
        """Clip the action to the valid range."""
        return np.clip(action, self.action_space.low, self.action_space.high)


class RunningMeanStd:
    """Calculate running mean and standard deviation."""
    
    def __init__(self, shape=(), epsilon=1e-4):
        """Initialize running statistics."""
        self.mean = np.zeros(shape, dtype=np.float64)
        self.var = np.ones(shape, dtype=np.float64)
        self.count = epsilon
    
    def update(self, x):
        """Update running statistics with new data."""
        batch_mean = np.mean(x, axis=0)
        batch_var = np.var(x, axis=0)
        batch_count = x.shape[0]
        self.update_from_moments(batch_mean, batch_var, batch_count)
    
    def update_from_moments(self, batch_mean, batch_var, batch_count):
        """Update from batch statistics."""
        delta = batch_mean - self.mean
        tot_count = self.count + batch_count
        
        new_mean = self.mean + delta * batch_count / tot_count
        m_a = self.var * self.count
        m_b = batch_var * batch_count
        M2 = m_a + m_b + np.square(delta) * self.count * batch_count / tot_count
        new_var = M2 / tot_count
        
        self.mean = new_mean
        self.var = new_var
        self.count = tot_count


def get_env_info(env_name: str) -> Dict[str, Any]:
    """
    Get information about an environment.
    
    Args:
        env_name: Environment name
        
    Returns:
        Dictionary with environment information
    """
    try:
        env = gym.make(env_name)
        
        info = {
            'name': env_name,
            'observation_space': {
                'type': str(type(env.observation_space).__name__),
                'shape': getattr(env.observation_space, 'shape', None),
                'low': getattr(env.observation_space, 'low', None),
                'high': getattr(env.observation_space, 'high', None),
                'n': getattr(env.observation_space, 'n', None)
            },
            'action_space': {
                'type': str(type(env.action_space).__name__),
                'shape': getattr(env.action_space, 'shape', None),
                'low': getattr(env.action_space, 'low', None),
                'high': getattr(env.action_space, 'high', None),
                'n': getattr(env.action_space, 'n', None)
            },
            'reward_range': env.reward_range,
            'max_episode_steps': getattr(env, '_max_episode_steps', None)
        }
        
        env.close()
        return info
        
    except Exception as e:
        return {'error': str(e)}


# Popular environment presets
ENV_PRESETS = {
    'classic_control': [
        'CartPole-v1',
        'MountainCar-v0',
        'Acrobot-v1',
        'Pendulum-v1'
    ],
    'box2d': [
        'LunarLander-v2',
        'BipedalWalker-v3',
        'CarRacing-v2'
    ],
    'atari': [
        'ALE/Breakout-v5',
        'ALE/Pong-v5',
        'ALE/SpaceInvaders-v5'
    ]
}


def list_environments(category: Optional[str] = None) -> list:
    """
    List available environments.
    
    Args:
        category: Optional category filter
        
    Returns:
        List of environment names
    """
    if category and category in ENV_PRESETS:
        return ENV_PRESETS[category]
    elif category:
        raise ValueError(f"Unknown category '{category}'. Available: {list(ENV_PRESETS.keys())}")
    else:
        # Return all environments
        all_envs = []
        for envs in ENV_PRESETS.values():
            all_envs.extend(envs)
        return all_envs


__all__ = [
    'make_env', 
    'apply_wrappers', 
    'get_env_info', 
    'list_environments',
    'NormalizeObservation',
    'ClipAction',
    'ENV_PRESETS'
]