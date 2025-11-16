cuadrados :: [Int]
cuadrados = [x^2 | x <- [1..10]]

main :: IO ()
main = print cuadrados
