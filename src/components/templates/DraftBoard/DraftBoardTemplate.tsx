/**
 * Displays all players, their statuses, and allows for drafting interaction.
 * CountdownBox, DraftQueue, PlayerCard, PlayersTable, TeamsTable, DraftResultsTable, MyFavourites, MyTeam, Updates
 * @returns
 */
import "./DraftBoardTemplate.scss";
import CountdownBox from "../../organisms/CountdownBox/CountdownBox";
import DraftQueue from "../../organisms/DraftQueue/DraftQueue";
import PlayerCard from "../../molecules/PlayerCard/PlayerCard";
import PlayersTable from "../../organisms/PlayersTable/PlayersTable";
import TeamsTable from "../../organisms/TeamsTable/TeamsTable";
import DraftResultsTable from "../../organisms/DraftResultsTable/DraftResultsTable";
import MyFavourites from "../../organisms/MyFavourites/MyFavourites";
import MyTeam from "../../organisms/MyTeam/MyTeam";
const DraftBoardTemplate = () => {
  return (
    <div className="draft-board">
      <div className="draft-board__sidebar">
        <CountdownBox />
        <DraftQueue />
      </div>
      <div className="draft-board__board">
        <PlayerCard />
        <div className="tables">
          <PlayersTable />
          <TeamsTable />
          <DraftResultsTable />
        </div>
      </div>
      <aside className="draft-board__personal">
        <MyFavourites />
        <MyTeam />
      </aside>
    </div>
  );
};

export default DraftBoardTemplate;
