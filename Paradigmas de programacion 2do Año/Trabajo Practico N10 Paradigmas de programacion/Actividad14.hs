vocales :: String -> String
vocales texto = [c | c <- texto, c `elem` "aeiouAEIOU"]

main :: IO ()
main = print (vocales "Hola mundo")