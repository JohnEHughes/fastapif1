import React from "react";
import { render } from 'react-dom';
import { ChakraProvider } from "@chakra-ui/react";

import Header from "./components/Header";
import Drivers from "./components/Drivers"; 

function App() {
  return (
    <ChakraProvider>
      <Header />
      <Drivers />
    </ChakraProvider>
  )
}

const rootElement = document.getElementById("root")
render(<App />, rootElement)