import {View, Text, TextInput, Button, FlatList} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { router, useRouter } from "expo-router";
import { AppInput } from "@/components/app-input";
import { AppButton } from "@/components/app-button";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import validator from "validator";

type User = {first_name:string,last_name:string, email:string};
export default function Profile() {

    const [user, setUser] = useState<User>({first_name:"", last_name:"", email:""})
    const router = useRouter();
    //fetch
    const fetchUser = async () =>{
        try {
            const res = await api.get("/users/me");
            setUser(res.data);
        } catch (error) {
         console.log("failed to fetch user")   
        }
    }

    useEffect(()=>{
        fetchUser()
    },[]);

    const UpdateUser = async () => {
        if(validator.isEmpty(user.first_name.trim())){
            alert("First name is required");
            return;
        }
        if(validator.isEmpty(user.last_name.trim())){
            alert("Last name is required");
            return;
        }
        if(validator.isEmpty(user.email.trim())){
            alert("email is required");
            return;
        }    
        if(!validator.isEmail(user.email)){
            alert("Enter a valid Email");
            return;
        }      
 
        try {
            await api.put("/users/me", {first_name:user.first_name, last_name:user.last_name, email:user.email})
            fetchUser();
            router.back();
        } catch (error) {
            console.log("failed to update user")   
        }
    }
    
    const deleteAccount = async ()=>{
        try {
            await api.delete(`/users/me`);
            router.replace("/login"); //redirect to login
        } catch (error) {
            console.log("failed to delete user") 
        }
    }

    return (

                <ScreenWrapper>
                    <ScreenHeader title="Account Details"></ScreenHeader>
                    {/*form*/}
                    <AppInput
                    label="First Name"
                    value ={user.first_name}
                    onChangeText={(text)=> setUser( {...user, first_name:text})}
                    />
                    <AppInput
                    label="Last Name"
                    value ={user.last_name}
                    onChangeText={(text)=> setUser({...user, last_name:text})}
                    />
                    <AppInput
                    label="Email"
                    value ={user.email}
                    onChangeText={(text)=>setUser({...user,email:text})}
                    />
                    <ButtomButtonContainer>
                    <AppButton
                    title="Delete Account" color="#c43232" onPress={deleteAccount}/>
                    <AppButton
                    title="Save"
                    color="#3d7fdb"
                    onPress={UpdateUser}
                    />
                    </ButtomButtonContainer>
                </ScreenWrapper>
    )

}