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

export default function EditCaregiver() {

        const[firstName, setFirstName] = useState<string>("");
        const[lastName, setLastName] = useState<string>("");
        const[email, setEmail] = useState<string>("");
        const {caregiver_id} = useLocalSearchParams();
        const router = useRouter();


        const fetchcaregiver = async () => {
            try {
                const res = await api.get(`/caregivers/me/${caregiver_id}`);
                
                const caregiver = res.data;    
                //reset input forms
                setFirstName(caregiver.first_name);
                setLastName(caregiver.last_name);
                setEmail(caregiver.email);
            } catch (error) {
                console.log("failed to fetch med")
            }
        };
        const updateCaregiver = async () => {
            if(validator.isEmpty(firstName.trim())){
                alert("First name is required");
                return;
            }
            if(validator.isEmpty(lastName.trim())){
                alert("Last name is required");
                return;
            }  
            if(validator.isEmpty(email.trim())){
                alert("Email is required");
                return;
            }  
            if(!validator.isEmail(email)){
                alert("Enter a valid Email");
                return;
            } 
            try {
                await api.put("/caregivers", {id: caregiver_id,first_name:firstName, last_name:lastName, contact_email:email})
                router.push("/(tabs)/Settings/caregiver")
            } catch (error) {
                console.log("failed to create caregiver")   
            }
        }
        useEffect(()=>{
            fetchcaregiver();
        },[])


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
            title="Update Caregiver"
            onPress={updateCaregiver}
            />
            </ButtomButtonContainer>
        </ScreenWrapper>
        );
    }