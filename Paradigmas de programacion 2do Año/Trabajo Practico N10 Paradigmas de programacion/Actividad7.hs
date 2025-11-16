paresSinCuatro :: [Int]
paresSinCuatro = [x | x <- [1..50], even x, x `mod` 4 /= 0]

main :: IO ()
main = print paresSinCuatro