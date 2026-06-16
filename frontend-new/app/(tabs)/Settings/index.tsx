
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import api from "@/lib/api";
import { useRouter } from "expo-router";
import { AppInput } from "@/components/app-input";
import { AppButton } from "@/components/app-button";
import { AppCard } from "@/components/card";
import { ButtomButtonContainer } from "@/components/buttomButtonContainer";
import {ScrollView, Text, View} from "react-native";
import { SettingsItems } from "@/components/setting_items";

export default function Settings(){
    const router = useRouter();

    const logout = async () => {
        try {
            await api.post("/logout");
            router.replace("/(auth)/login");
        } catch (error) {
            console.log("logout failed");
        }
    }

    return (
        <ScreenWrapper>
            <ScreenHeader title="Settings" showBackArrow={false}/>
            <SettingsItems title= "Profile" onPress={()=>router.push("./Settings/profile")}/>
            <SettingsItems title= "Caregivers" onPress={()=>router.push("/(tabs)/Settings/caregiver")}/>
            <SettingsItems title= "Habits" onPress={()=>router.push("/(tabs)/Settings/habit")}/>
            <ScrollView style={{margin:12 }}>
                <Text style={{fontSize:18, fontWeight:"600"}}>Understanding Your Data</Text>
                <Text style={{marginTop:8,marginBottom:8}}>Missed doses are automatically logged after a 60-minute grace window period from the scheduled time.</Text>
                <Text style={{marginBottom:8}}>Your Adherence risk is calculated using a rolling 14-day window to provide timely insights.</Text>
                <Text style={{marginBottom:8}}>Caregivers receive email alerts only when a adherence risk is detected.</Text>
                <Text>Streaks are calculated per medication and are only displayed on Home screen.</Text>
            </ScrollView>
            
            <ButtomButtonContainer>
            <AppButton title="Logout" color="#c74343" onPress={logout}/>
            </ButtomButtonContainer>
        </ScreenWrapper>
    );


}