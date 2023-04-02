import React, { useEffect, useState } from "react";
import {
    Box,
    Button,
    Flex,
    Input,
    InputGroup,
    Modal,
    ModalBody,
    ModalCloseButton,
    ModalContent,
    ModalFooter,
    ModalHeader,
    ModalOverlay,
    Stack,
    Text,
    useDisclosure
} from "@chakra-ui/react";


const DriversContext = React.createContext({
    drivers: [], fetchDrivers: () => {}
  })

  export default function Drivers() {
    const [drivers, setDrivers] = useState([])

    const fetchDrivers = async () => {
      const response = await fetch("http://localhost:8000/drivers")
      const drivers = await response.json()
      setDrivers(drivers.data)
    }
    useEffect(() => {
        fetchDrivers()
    }, [])
    return (
        <DriversContext.Provider value={{drivers, fetchDrivers}}>
            <AddDriver />
            <Stack spacing={1}>
                <br></br>
                {drivers.map((driver) => (
                <DriverHelper first_name={
                    driver.first_name}
                    last_name={driver.last_name} 
                    age={driver.age} 
                    is_active={String(driver.is_active)} 
                    id={driver.id}
                    FetchDrivers={fetchDrivers} />
                ))}
            </Stack>

        </DriversContext.Provider>
    )
}

function AddDriver() {
    const [first_name, setFirstName] = React.useState("")
    const [last_name, setLastName] = React.useState("")
    const [age, setAge] = React.useState("")
    const [is_active, setActive] = React.useState("")

    const {drivers, fetchDrivers} = React.useContext(DriversContext)
  
    const handleFirstName = event  => {
        setFirstName(event.target.value)
    }
    const handleLastName = event  => {
        setLastName(event.target.value)
    }
    const handleAge = event  => {
        setAge(event.target.value)
    }
    const handleActive = event  => {
        setActive(event.target.value)
    }
  
    const handleSubmit = (event) => {
      const newDriver = {
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "is_active": is_active
      }
  
      fetch("http://localhost:8000/drivers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newDriver)
      }).then(fetchDrivers)
    }
  
    return (
      <div><form onSubmit={handleSubmit}>
        <InputGroup size="md" pr="4.5rem">
          <Input
            type="text"
            value={first_name}
            placeholder="Add a Driver first name"
            aria-label="Add a Driver first name"
            onChange={handleFirstName}
          />
        <Input
            type="text"
            value={last_name}
            placeholder="Add a Driver last name"
            aria-label="Add a Driver last name"
            onChange={handleLastName}
          />
        <Input
            type="number"
            value={age}
            placeholder="Add a Driver age"
            aria-label="Add a Driver age"
            onChange={handleAge}
          />
        <Input
            type="text"
            value={is_active}
            placeholder="Add a Driver's active status - true/false"
            aria-label="Add a Driver's active status - true/false"
            onChange={handleActive}
          />
        </InputGroup>
        <Button type="submit">Submit</Button>
      </form>
      <br></br>
      <b>DRIVERS IN THE DATABASE:</b>
      </div>
    )
  }

  function DeleteDriver({id}) {
    const {fetchDrivers} = React.useContext(DriversContext)
  
    const deleteDriver = async () => {
      await fetch(`http://localhost:8000/drivers/${id}`, {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: { "id": id }
      })
      await fetchDrivers()
    }
  
    return (
      <Button h="1.5rem" size="sm" onClick={deleteDriver}>Delete Driver</Button>
    )
  }

  function DriverHelper({first_name, last_name, age, is_active, id, fetchDrivers}) {
    return (
      <Box p={1} shadow="sm">
        <Flex justify="space-between">
          <Text mt={4} as="div">
            name: {first_name} {last_name}, <br></br>
            age: {age}yrs, <br></br>
            active: {is_active}, <br></br>
            driver_id: {id}
            <Flex align="end">
              <DeleteDriver id={id} fetchDrivers={fetchDrivers}/>
            </Flex>
          </Text>
        </Flex>
      </Box>
    )
  }