multiplos235 :: [Int]
multiplos235 = [x | x <- [1..100], x `mod` 2 == 0, x `mod` 3 == 0, x `mod` 5 == 0]

main :: IO ()
main = print multiplos235