mayoriaEdadv1 :: [Int] -> [String]
mayoriaEdadv1 edades = map evaluar edades
  where
    evaluar e = if e >= 18 then "Mayor" else "Menor"

mayoriaEdadv2 :: [Int] -> [String]
mayoriaEdadv2 edades = map (\e -> if e >= 18 then "Mayor" else "Menor") edades

main :: IO ()
main = do
    print (mayoriaEdadv1 [5, 20, 18, 10])
    print (mayoriaEdadv2 [5, 20, 18, 10])
