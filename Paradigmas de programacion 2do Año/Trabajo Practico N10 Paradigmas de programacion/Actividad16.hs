mizip :: [a] -> [b] -> [(a, b)]
mizip xs ys = [(x, y) | (x, y, _) <- zip3 xs ys [1..min (length xs) (length ys)]]

main :: IO ()
main = print (mizip [1,2,3] [9,9,9])