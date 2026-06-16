import {View, Text, TextInput, Button, FlatList} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useEffect, useState} from "react";
import api from "@/lib/api";
import { useRouter } from "expo-router";
import { useLocalSearchParams } from "expo-router";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import validator from "validator";

export default function EditMedication() {

        const [name, setName] = useState("");
        const [amount, setAmount] = useState("");
        const [doseUnit, setDoseUnit] = useState("");
        const {medication_id} = useLocalSearchParams();
        const router = useRouter();

        const fetchMed = async () => {
            try {
                const res = await api.get(`/medications/me/${medication_id}`);
                
                const med = res.data;    
                //reset input forms
                setName(med.name);
                setAmount(String(med.amount));
                setDoseUnit(med.dose_unit);
            } catch (error) {
                console.log("failed to fetch med")
            }
        };
        // get med info when screen load
        useEffect(()=>{
            fetchMed();
        }, []);

        const updateMed = async () => {
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
                await api.put("/medications", {
                    id: medication_id,name, amount: Number(amount), dose_unit:doseUnit
                })
                router.back();
            } catch (error) {
                console.log("failed to update med")
            }
        };
        return (
            <ScreenWrapper><ScreenHeader  title="Edit Medication"/>
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
            <AppButton title="Save Changes" onPress={updateMed}/>
            </ButtomButtonContainer>
            </ScreenWrapper>
        );
    }