import {FlatList,View, TouchableOpacity, Switch} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useEffect, useState} from "react";
import api from "@/lib/api";import { AppButton } from "@/components/app-button";
import { ListItem } from "@/components/list-item-card";
import { useRouter } from "expo-router";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";



type Caregiver = {id:number, first_name:string,last_name:string, email:string, notify:boolean};

export default function CaregiverList(){
    const [caregivers, setCaregivers] = useState<Caregiver[]>([]);
    //fetch
    const fetchCaregivers = async () =>{
        try {
            const res = await api.get("/caregivers");
            setCaregivers(res.data);
        } catch (error) {
         console.log("failed to fetch caregivers")   
        }
    }
    const router = useRouter();

    useEffect(()=>{
        fetchCaregivers()
    },[]);

    const deleteCaregiver = async (caregiver_id:number)=>{
        try {
            await api.delete(`/caregivers/${caregiver_id}`)
            fetchCaregivers();
        } catch (error) {
            console.log("failed to delete caregiver") 
        }
    }
    const toggleCaregiver = async (caregiver_id:number)=>{
    try {
        await api.post(`/caregivers/${caregiver_id}/toggle`)
        
        fetchCaregivers();
    } catch (error) {
        console.log("failed to toggle caregiver") 
    }
    }
    return(
        <ScreenWrapper>
            <ScreenHeader title="Caregivers"></ScreenHeader>

            {/*list*/}
            <FlatList
            data={caregivers}
            keyExtractor = {item => item.id.toString()}
            renderItem={({item})=>{
                return (
                    <ListItem
                    title = {item.first_name}
                    subtitle={item.last_name}
                    right={
                    <View style={{flexDirection:"row", gap:10, padding:5}}>
                    <MaterialIcons name="delete"
                    size={20}
                    color="#cf4040"
                    onPress={()=>deleteCaregiver(item.id)}/>
                    <MaterialIcons name="edit"
                    size={20}
                    color="#838383"
                    onPress={()=>{router.push({pathname: "/(tabs)/Settings/caregiver/edit_caregiver", params:{caregiver_id: item.id} })}}/>
                    <Switch
                    value={item.notify}
                    onValueChange={()=>toggleCaregiver(item.id)}/>
                    </View>
                    }
                    />
                )

            }}
            />

        <TouchableOpacity
        onPress={()=>{router.push("/(tabs)/Settings/caregiver/add_caregiver")}}
        style={{
            position:"absolute", bottom: 20, 
            right: 20, backgroundColor: "#3d7fdb", 
            width:50, height:50, borderRadius: 25, 
            justifyContent:"center", alignItems:"center",
        }}
        >
           <MaterialIcons name="add" size={20} color="white"/>
        </TouchableOpacity>
        </ScreenWrapper>

    )
}     