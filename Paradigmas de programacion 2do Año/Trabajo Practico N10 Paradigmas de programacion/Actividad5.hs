cubos :: [Int]
cubos = [x^3 | x <- [1..10]]

main :: IO ()
main = print cubos