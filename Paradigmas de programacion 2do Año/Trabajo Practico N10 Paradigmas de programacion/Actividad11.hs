paresSumaMenor20 :: [(Int, Int)]
paresSumaMenor20 = [(x, y) | x <- [1..20], y <- [1..20], x + y <= 20]

main :: IO ()
main = print paresSumaMenor20