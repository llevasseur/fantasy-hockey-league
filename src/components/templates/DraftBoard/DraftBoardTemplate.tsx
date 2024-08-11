/**
 * Displays all players, their statuses, and allows for drafting interaction.
 * CountdownBox, DraftQueue, PlayerCard, PlayersTable, TeamsTable, DraftResultsTable, MyFavourites, MyTeam, Updates
 * @returns
 */
import CountdownBox from "../../organisms/CountdownBox/CountdownBox";
import DraftQueue from "../../organisms/DraftQueue/DraftQueue";
import PlayerCard from "../../molecules/PlayerCard/PlayerCard";
import PlayersTable from "../../molecules/PlayerCard/PlayerCard";
import TeamsTable from "../../organisms/TeamsTable/TeamsTable";
import DraftResultsTable from "../../organisms/DraftResultsTable/DraftResultsTable";
import MyFavourites from "../../organisms/MyFavourites/MyFavourites";
import MyTeam from "../../organisms/MyTeam/MyTeam";
const DraftBoardTemplate = () => {
  return (
    <div>
      <CountdownBox />
      <DraftQueue />
      <PlayerCard />
      <PlayersTable />
      <TeamsTable />
      <DraftResultsTable />
      <MyFavourites />
      <MyTeam />
      DraftBoardTemplate
    </div>
  );
};

export default DraftBoardTemplate;
