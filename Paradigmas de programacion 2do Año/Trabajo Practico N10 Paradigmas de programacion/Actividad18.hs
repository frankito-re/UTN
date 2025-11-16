soloNegativosv1 :: [Int] -> [Int]
soloNegativosv1 xs = filter esNegativo xs
  where
    esNegativo x = x < 0

soloNegativosv2 :: [Int] -> [Int]
soloNegativosv2 xs = filter (\x -> x < 0) xs

main :: IO ()
main = do
    print (soloNegativosv1 [5, -3, 0, -8, 10])
    print (soloNegativosv2 [5, -3, 0, -8, 10])