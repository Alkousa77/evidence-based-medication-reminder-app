import {useState} from "react";
import {View, Text, Platform} from "react-native";
import {router} from "expo-router";
import api from "../../lib/api";
import ScreenWrapper from "../../components/ScreenWrapper";
import * as Device from "expo-device";
import * as Notifications from "expo-notifications";
import Constants from "expo-constants";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import validator from "validator";


export default function Login() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    
    const handleLogin = async () => {
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
            await api.post("/login", {email, password});
            //call puysh notifiaiton method on non web platforms
            if (Platform.OS !== "web"){
                await registerForPushNotificationsAsync();}
            router.replace("/(tabs)/home");
        } catch (error:any) {
            if (error.response?.status === 401){
                alert ("invalid email or password")}
            else {
            alert("someting went wrong")
        }
    }
    }
    async function registerForPushNotificationsAsync() {
        if (Platform.OS === "android"){
            //Android requries cahnnels (channelId, channel name, high notification importance)
            await Notifications.setNotificationChannelAsync("medication_reminders", {name: "Medication Reminders", importance: Notifications.AndroidImportance.MAX,});
        }
        // ensure real phone 
        if (!Device.isDevice) {
        alert('Must use a real device for push notifications')
        return; 
        }
        //check existing permision
        const {status: existingStatus} = await Notifications.getPermissionsAsync(); 

         //if no existing premission, request permission 
        if (existingStatus !== "granted") {
        const {status} = await Notifications.requestPermissionsAsync(); 
        //if not granted premission after asking, stop
        if (status !== "granted") return;
        }
        //get projectId from app.json
        const projectId = Constants.expoConfig?.extra?.eas?.projectId;
        const tokenData = await Notifications.getExpoPushTokenAsync({projectId}); // contact expo server get token to identify device
        const token = tokenData.data //extract token

        //send token to backend (update user record)
        await api.post("/users/push-token", {token})
    };

    return(
        <ScreenWrapper> 
            <View style={{margin:40, alignItems:"center"}}>
            <MaterialCommunityIcons name="pill" size={35} color="#499bdf"/>
            <Text style={{fontSize:30, fontWeight:600}}> Welcome Back</Text>
            </View>
        <View style={{padding:20}}>
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

            <AppButton title="Login" onPress={handleLogin}/>
            
            <AppButton title="Register" color= "#4b5761" onPress={()=> router.push("/(auth)/register")}/>
        </View>
        </ScreenWrapper>
    );
}
