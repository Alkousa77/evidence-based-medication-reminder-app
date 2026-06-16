import {View, Text, TextInput, Button, FlatList} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useEffect, useState} from "react";
import api from "@/lib/api";
import { useRouter } from "expo-router";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import {ButtomButtonContainer} from "@/components/buttomButtonContainer"
import validator from "validator";

export default function AddMedications() {

        const [name, setName] = useState("");
        const [amount, setAmount] = useState("");
        const [doseUnit, setDoseUnit] = useState("");
        
        const router = useRouter();

        const createMed = async () => {
            if(validator.isEmpty(name.trim())){
                alert("Medication name is required");
                return;
            }
            if(validator.isEmpty(amount)){
                alert("Medication amount is required");
                return;
            }  
            if(!validator.isNumeric(amount)){
                alert("Amount must be a number");
                return;
            }      
            if(validator.isEmpty(doseUnit.trim())){
                alert("Dose unit is required");
                return;
            }  
            try {
                const res = await api.post("/medications", {
                    name, amount: Number(amount), dose_unit:doseUnit
                })

            const createdMed = res.data;    
            //reset input forms
            setName("");
            setAmount("");
            setDoseUnit("");
            
            //navigate to schedule screen with med id
            router.push({
                pathname: "./schedule",
                params: {medication_id: createdMed.id}
            })
            } catch (error) {
                console.log("failed to create med")
            }
        };
        return (
            <ScreenWrapper><ScreenHeader  title="Add Medication"/>
                {/*Create form*/}

            <Text>Name</Text>
            <AppInput 
            value={name}
            onChangeText={setName}/>
            <Text>Amount</Text>
            <AppInput 
            value={amount}
            onChangeText={setAmount}/>
            <Text>Dose Unit</Text>
            <AppInput 
            value={doseUnit}
            onChangeText={setDoseUnit}/>
            <ButtomButtonContainer>
                <AppButton title="Next: Schedule" onPress={createMed}/>
            </ButtomButtonContainer>


            </ScreenWrapper>
        );
    }