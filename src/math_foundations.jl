# src/math_foundations.jl

"""
Mathematical Foundations for Alpamayo R1 Autonomous Driving

This module contains the core mathematical equations referenced during
the reasoning and decision-making pipeline. While the core application
is in Python, these pure mathematical models in Julia serve as the 
ground truth for verifying physical bounds and planning trajectories.
"""
module MathFoundations

export kinematic_bicycle_step, pure_pursuit_steering, pid_control, time_to_collision

"""
    kinematic_bicycle_step(x, y, θ, v, δ, L, dt)

Calculates the next state of a vehicle using the Kinematic Bicycle Model.

# Arguments
- `x::Float64`: Current X position (m)
- `y::Float64`: Current Y position (m)
- `θ::Float64`: Current heading (radians)
- `v::Float64`: Velocity (m/s)
- `δ::Float64`: Steering angle (radians)
- `L::Float64`: Wheelbase of the vehicle (m)
- `dt::Float64`: Time step (s)

# Returns
- A tuple `(next_x, next_y, next_θ)` representing the state after `dt`.
"""
function kinematic_bicycle_step(x::Float64, y::Float64, θ::Float64, v::Float64, δ::Float64, L::Float64, dt::Float64)
    # Rate of change
    dx = v * cos(θ)
    dy = v * sin(θ)
    dθ = (v / L) * tan(δ)
    
    # Simple Euler integration
    next_x = x + dx * dt
    next_y = y + dy * dt
    next_θ = θ + dθ * dt
    
    return (next_x, next_y, next_θ)
end

"""
    pure_pursuit_steering(rx, ry, current_x, current_y, current_θ, L)

Calculates the steering angle required to reach a lookahead point.

# Arguments
- `rx::Float64`: Target X position (m)
- `ry::Float64`: Target Y position (m)
- `current_x::Float64`: Vehicle X position (m)
- `current_y::Float64`: Vehicle Y position (m)
- `current_θ::Float64`: Vehicle heading (radians)
- `L::Float64`: Wheelbase of the vehicle (m)

# Returns
- `δ::Float64`: Calculated steering angle (radians)
"""
function pure_pursuit_steering(rx::Float64, ry::Float64, current_x::Float64, current_y::Float64, current_θ::Float64, L::Float64)
    # Compute relative angle to target (alpha)
    dx = rx - current_x
    dy = ry - current_y
    alpha = atan(dy, dx) - current_θ
    
    # Distance to target (l_d)
    l_d = sqrt(dx^2 + dy^2)
    
    if l_d == 0.0
        return 0.0
    end
    
    # Pure pursuit standard formula: δ = atan(2 * L * sin(alpha) / l_d)
    δ = atan((2 * L * sin(alpha)) / l_d)
    return δ
end

"""
    pid_control(target, current, kp, ki, kd, &integral_err, prev_err, dt)

A generic Proportional-Integral-Derivative controller for maintaining speed or position.
Returns the required control effort.
"""
function pid_control(target::Float64, current::Float64, kp::Float64, ki::Float64, kd::Float64, integral_err::Float64, prev_err::Float64, dt::Float64)
    error = target - current
    
    p = kp * error
    new_integral_err = integral_err + (error * dt)
    i = ki * new_integral_err
    d = kd * ((error - prev_err) / dt)
    
    output = p + i + d
    
    return output, new_integral_err, error
end

"""
    time_to_collision(v_ego, v_target, distance)

Calculates standard TTC (Time To Collision) in a 1D car-following scenario.
Returns Inf if the ego vehicle is slower.
"""
function time_to_collision(v_ego::Float64, v_target::Float64, distance::Float64)
    relative_speed = v_ego - v_target
    if relative_speed <= 0
        return Inf
    end
    return distance / relative_speed
end

end # module MathFoundations
