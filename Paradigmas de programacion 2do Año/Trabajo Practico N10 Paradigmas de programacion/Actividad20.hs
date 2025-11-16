inversav1 :: [String] -> [String]
inversav1 palabras = map reverse palabras

inversav2 :: [String] -> [String]
inversav2 = map (\p -> reverse p)

main :: IO ()
main = do
    print (inversav1 ["hola","mundo"])
    print (inversav2 ["hola","mundo"])