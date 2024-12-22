function main(u, v) begin
    # Variable declaration
    x = 5 y = 10

    # Some mathematical expressions
    x = x + 1
    y = y - 2
    z = x * y
    a = y / x
    
    # Comparison operators
    if (x < y) begin
        x = x + 1
    end
    
    if (x <= y) begin
        x = x - 1
    else
        y = y + 1
    end
    
    if (x == y) begin
        x = x * 2
    end
    
    # Logical operators
    if (x and y) begin
        return x;
    end
    if (x or y) begin
        return y;
    end
    if (not x) begin
        return 0;
    end
    
    # While loop
    while (x <= y) begin
        x = x + 1;
    end
    
    # Function call with arguments
    int result = add(3, 4);
    
    # Strings and function definition
    string greeting = "Hello, world!";
    string reply = "Hi!";
    
    # Return statement
    return x;
end

# A function definition example
function add(a, b) begin
    return a + b
end

# Another function that uses return
function subtract(a, b) begin
    return a - b
begin

# Invalid token example (wrong token)
;
\
?
&
%
