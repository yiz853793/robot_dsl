# Function definitions and assignments to test the interpreter

# Function to calculate factorial
function factorial(n) begin
    if (n == 0) begin
        return 1
    else
        return n * factorial(n - 1)
    end
end

# Function to test arithmetic operations
function calculate(a, b, c) begin    
    # Nested arithmetic operations
    result = (a + b) * (c - 2) / 3
    return result
end

# Main function with various operations
function main() begin
    x = 5
    y = 10
    z = 2
    
    # Arithmetic operations with variables
    x = x + y
    y = y - z
    
    # Nested function calls
    sum = calculate(x, y, z)
    
    # Factorial calculation and conditions
    fact = factorial(5)
    
    # Logical operations with conditions
    if (x > y and fact == 120) begin
        z = z + 1
    else if (y >= z or sum < 20) begin
            z = z - 1
        else 
            z = 0
        end
    end
    
    # Return a complex expression as a final result
    return (sum + fact) * (x - y) / z

    print('after function main return')
end

main()

# Function to handle string concatenation
function concatStrings(str1, str2) begin
    result = str1 + str2
    return result
end

# Test string concatenation
greeting = concatStrings("Hello, ", "world!")

# Final return from main
a = len(greeting)

print('print ',a[0],' charactors\n')

print('main\'s output is ', main(), '\n')

return greeting

print('after return')

