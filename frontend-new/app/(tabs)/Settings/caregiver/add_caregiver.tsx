import {View, Text, TextInput, Button, FlatList} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useEffect, useState} from "react";
import api from "@/lib/api";
import { useLocalSearchParams, useRouter } from "expo-router";
import { AppInput } from "@/components/app-input";
import { AppButton } from "@/components/app-button";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import validator from "validator";


export default function AddCaregiver() {

        const[firstName, setFirstName] = useState<string>("");
        const[lastName, setLastName] = useState<string>("");
        const[email, setEmail] = useState<string>("");
        const router = useRouter();

        const createCaregiver = async () => {
            if(validator.isEmpty(firstName.trim())){
                alert("First name is required");
                return;
            }
            if(validator.isEmpty(lastName.trim())){
                alert("Last name is required");
                return;
            }  
            if(validator.isEmpty(email.trim())){
                alert("email is required");
                return;
            }  
            if(!validator.isEmail(email)){
                alert("Enter a valid Email");
                return;
            }    
            try {
                await api.post("/caregivers", {first_name:firstName, last_name:lastName, contact_email:email})
                router.push("/(tabs)/Settings/caregiver")
            } catch (error) {
                console.log("failed to create caregiver")   
            }
        }

    return(
        <ScreenWrapper> 
            <ScreenHeader title="Caregivers"></ScreenHeader>
            {/*form*/}
            <AppInput
            label="First Name"
            value ={firstName}
            onChangeText={setFirstName}
            placeholder="Reem"
            />
            <AppInput
            label="Last Name"
            value ={lastName}
            onChangeText={setLastName}
            placeholder="Rany"
            />
            <AppInput
            label="Email"
            value ={email}
            onChangeText={setEmail}
            placeholder="Reem@example.com"
            />
            <ButtomButtonContainer>
            <AppButton 
            title="Add Caregiver"
            onPress={createCaregiver}
            />
            </ButtomButtonContainer>
        </ScreenWrapper>
        );
    }