/**
 * Dynamic box for Timer and Round details, pick details, Overall number
 * Detail who's turn it is and how far "User's" turn is
 */
import "./CountdownBox.scss";
import Timer from "../../atoms/Timer/Timer";
import PlayerNext from "../../molecules/PlayerNext/PlayerNext";

const CountdownBox = () => {
  return (
    <div className="countdown-box">
      <Timer />
      <PlayerNext />
    </div>
  );
};

export default CountdownBox;
