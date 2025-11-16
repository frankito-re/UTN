impares :: [Int]
impares = [2*x - 1 | x <- [1..10]]

main :: IO ()
main = print impares
