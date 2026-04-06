# API Orchestration Environment for AI Agents

## Overview
This project simulates a real-world API orchestration system where an AI agent must complete multi-step workflows under uncertainty.

## Problem
Modern systems rely on multiple APIs (authentication, payments, notifications). These APIs can fail, require retries, and have dependencies.

## Environment Design

### Observation
- pending_tasks
- completed_tasks
- api_status
- last_error
- step_count

### Actions
- call_auth_api
- call_payment_api
- call_notify_api
- retry
- abort

### Reward
- Successful API call: positive reward
- Failure: negative reward
- Retry success: bonus
- Full workflow: high cumulative reward

## Tasks

### Easy
- No failures

### Medium
- Random API failures

### Hard
- Dependency constraints + failure handling

## Example Run

[STEP] call_auth_api → reward 0.2  
[STEP] call_payment_api → reward 0.4  
[STEP] call_notify_api → reward 0.2  

Final Score: 0.8

## Key Features
- Handles uncertainty (failures, retries)
- Real-world API workflow simulation
- Decision-based environment for LLM agents