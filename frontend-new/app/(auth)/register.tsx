import React, {useState} from "react";
import {View, Text, TextInput} from "react-native";
import {router} from "expo-router";
import api from "../../lib/api";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import ScreenWrapper from "@/components/ScreenWrapper";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import validator from "validator";

export default function Register() {

    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    
    const handleRegister = async () => {
        if (validator.isEmpty(firstName.trim())){
            alert("First Name is required");
            return;
        }
        if (validator.isEmpty(lastName.trim())){
            alert("Last Name is required");
            return;
        }
        if(validator.isEmpty(email.trim())){
            alert("email is required");
            return;
        }  
        if (!validator.isEmail(email)){
            alert("Enter a valid email");
            return;
        }
        if (validator.isEmpty(password.trim())){
            alert("Password is required");
            return;
        }
        try {
            await api.post("/signup", {
                email, password,
                first_name: firstName, last_name:lastName});
            router.replace("/login");
        } catch (error:any) {
            alert(error.response?.data?.error ||"could not create account")
        }
    };

    return(
        <ScreenWrapper>
            <View style={{margin:40, alignItems:"center"}}>
            <MaterialCommunityIcons name="pill" size={35} color="#499bdf"/>
            <Text style={{fontSize:30, fontWeight:600}}>Create Account</Text>
            </View>
            <Text>
                First Name
            </Text>
            <AppInput
            value={firstName}
            onChangeText={setFirstName}
            />
            <Text>
                Last Name
            </Text>
            <AppInput
            value={lastName}
            onChangeText={setLastName}
            />
            <Text>
                Email
            </Text>
            <AppInput
            value={email}
            onChangeText={setEmail}
            />

            <Text>
                Password
            </Text>
            <AppInput
            value={password}
            onChangeText={setPassword}
            secureTextEntry
            />

            <AppButton title="Register" onPress={handleRegister}/>
        </ScreenWrapper>
    )

}
