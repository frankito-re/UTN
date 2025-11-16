pares :: [Int]
pares = [x | x <- [1..20], even x]

main :: IO ()
main = print pares
