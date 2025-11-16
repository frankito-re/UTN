longitudes :: [String] -> [Int]
longitudes palabras = [length palabra | palabra <- palabras]

main :: IO ()
main = print (longitudes ["hola", "adiós", "Haskell"])