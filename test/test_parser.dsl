# Function definition

main()

function main() begin
    # Variable assignments
    x = 10
    y = 20
    
    # Arithmetic operations and comparisons
    x = x + y
    y = y - 5
    z = x * y
    a = y / x
    v = a + (b * c) - (d / 2) * (a + b)

    # array
    w = [1, 2, x, y]

    w[3] = u

    x = w[2]

    w = w * 2

    # If statement with comparison
    if (x < y) begin
        x = x + 1
    end
    
    if (x <= y) begin
        x = x - 1
    else
        b = c
    end
    
    # While loop with condition
    while (x < 50) begin
        x = x + 1
    end
    
    # Function calls
    result = add(x, y) + b + d
    return result
end

# A simple add function definition
function add(a, b) begin
    return a + b
end

# Another simple function with string handling
function greet() begin
    greeting = "Hello, world!"
    return greeting
end

# Function call with parameters
result = add(3, 4)

# Return statement for result
return result
