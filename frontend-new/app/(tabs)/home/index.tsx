import {View, Text, FlatList, TouchableOpacity} from "react-native";
import ScreenWrapper from "@/components/ScreenWrapper"
import ScreenHeader from "@/components/ScreenHeader"
import {useCallback, useEffect, useState} from "react";
import api from "@/lib/api";
import { useFocusEffect, useRouter } from "expo-router";
import { AppButton } from "@/components/app-button";
import { AppInput } from "@/components/app-input";
import { ListItem } from "@/components/list-item-card";
import { Banner } from "react-native-paper";
import { format } from "date-fns";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";


type streaks = {medication_id:number, current_streak:number}
type alerts = {medication_id:number, name:string}
type reminders = {medication_id : number, schedule_time_id: number,medication_name: string, next_due_at: string, habit_name?:string|null, }
export default function Home() {
    const [reminders, setReminders] = useState<reminders[]>([]);
    const [alerts, setAlerts] = useState<alerts[]>([]);
    const [streaks, setStreaks] = useState<streaks[]>([]);

    //fetch
    const fetchUpcoming = async () =>{
        try {
            const res = await api.get("/reminders");
            setReminders(res.data.reminders);
            setAlerts(res.data.alerts);
            setStreaks(res.data.streaks);

        } catch (error) {
         console.log("failed to fetch reminders")   
        }
    }

        useFocusEffect( 
            useCallback(()=>{
            fetchUpcoming();
        },[]))

    const handleTaken = async (reminder_id:number)=>{
        try {
            await api.post(`/doses/${reminder_id}/taken`)
            
            await fetchUpcoming();
        } catch (error) {
            console.log("failed to set Taken") 
        }}

        const  handleDismissed  =  async () => {
            try {
                await api.post("/reminders/dismiss", {medication_ids: alerts.map(a=>a.medication_id)});
                fetchUpcoming(); //update alerts
            } catch (error) {
                console.log("Failed to dismiss alerts")
            }
        }

    return(
        <ScreenWrapper>
        <ScreenHeader title = "Home" showBackArrow={false}/>

        {/*Alerts*/}
        <Banner
        style ={{marginBottom:15, backgroundColor: "#fd9292",borderRadius: 25}}
        visible={alerts.length>0}
        icon= "alert-circle"
        actions={[
            {label: "Dissmis",
            onPress:handleDismissed, // set dissmised alerts
        },
    ]}
        >
            {`Adherence risk detected for: ${alerts.map(alert=>alert.name).join(", ")}`}
        </Banner>
                
        <Text style={{fontSize:20, fontWeight: "600",paddingLeft:8}}>Upcoming Doses</Text>
        {/*list*/}
        <FlatList
        data={reminders}
        keyExtractor = {item => item.schedule_time_id.toString()}
        renderItem={({item})=>{
            return (
                <View style={{marginBottom:10}}>
                <ListItem
                direction="column"
                title = {`${item.medication_name} `}
                subtitle={`Next Dose: ${format(new Date(item.next_due_at), "EEE HH:mm")}`} 
                bottom={
                <>  
                        <Text style={{fontSize:13,fontWeight: "600", color:"#37b0e7"}}> Day Streak</Text>
                    <View style={{flexDirection:"row", alignItems:"center"}}>
                        <MaterialIcons name="local-fire-department"
                        size={20}
                        color="#37b0e7"/>           
                        <Text style={{fontSize:13,fontWeight: "600", color:"#37b0e7"}}>{streaks.find(s => s.medication_id === item.medication_id)?.current_streak??0}</Text> 
                    </View>
                    <TouchableOpacity onPress={()=>handleTaken(item.schedule_time_id)}
                       style={{backgroundColor:"#1f8dc0", padding:12, borderRadius:12, margin:10, alignItems:"center"}}>
                       <Text style={{color:"white", fontWeight:"600"}}>confirm Dose</Text>
                        
                    </TouchableOpacity> 
                    

                    
                </>
                }
                />
                </View>
            )

        }}
        />
        </ScreenWrapper>
    )
}