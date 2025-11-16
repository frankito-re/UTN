divTres :: [Int]
divTres = [3 * x | x <- [1..33]]

main :: IO ()
main = print divTres
