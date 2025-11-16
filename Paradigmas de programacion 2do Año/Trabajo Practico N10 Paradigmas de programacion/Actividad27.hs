moverPrimera :: String -> String
moverPrimera "" = ""              
moverPrimera (x:xs) = xs ++ [x]  

main :: IO ()
main = do
    print (moverPrimera "hola, sigue sin gustarme haskell")